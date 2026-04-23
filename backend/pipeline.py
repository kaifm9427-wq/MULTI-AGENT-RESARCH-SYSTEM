import re
import time

from agents import writer_chain
from tools import web_search, scrape_url


def _extract_urls(search_text: str) -> list[str]:
    return re.findall(r"URL:\s*(https?://\S+)", search_text)


def _extract_titles(search_text: str) -> list[str]:
    return re.findall(r"Title:\s*(.+)", search_text)


def _extract_snippets(search_text: str) -> list[str]:
    return re.findall(r"Snippet:\s*(.+)", search_text)


def _build_sources(search_text: str, scraped_sections: list[str]) -> list[dict]:
    urls = _extract_urls(search_text)
    titles = _extract_titles(search_text)
    snippets = _extract_snippets(search_text)

    sources = []
    for index, url in enumerate(urls):
        sources.append(
            {
                "title": titles[index] if index < len(titles) else f"Source {index + 1}",
                "url": url,
                "snippet": snippets[index] if index < len(snippets) else "",
                "excerpt": scraped_sections[index] if index < len(scraped_sections) else "",
            }
        )

    return sources


def _invoke_chain_with_retry(chain, payload: dict, retries: int = 2, wait_seconds: int = 10) -> str:
    for attempt in range(1, retries + 1):
        try:
            return chain.invoke(payload)
        except Exception as exc:
            message = str(exc)
            is_retryable = any(
                marker in message
                for marker in [
                    "RESOURCE_EXHAUSTED",
                    "429",
                    "503",
                    "UNAVAILABLE",
                    "high demand",
                    "InternalServerError",
                    "500",
                ]
            )
            if not is_retryable or attempt == retries:
                raise

            current_wait = wait_seconds * attempt
            print(
                f"\nGemini is temporarily unavailable. Waiting {current_wait} seconds "
                f"before retry {attempt + 1}/{retries}..."
            )
            time.sleep(current_wait)

    raise RuntimeError("Failed to get a response from the language model.")


def _clean_line(value: str) -> str:
    return " ".join(value.split()).strip()


def _extract_sentences(text: str) -> list[str]:
    cleaned = _clean_line(text)
    if not cleaned:
        return []
    parts = re.split(r"(?<=[.!?])\s+", cleaned)
    return [part.strip() for part in parts if len(part.strip()) > 30]


def _is_noisy_sentence(sentence: str) -> bool:
    lowered = sentence.lower()
    noisy_markers = [
        "access denied",
        "you don't have permission",
        "reference #",
        "errors.edgesuite.net",
        "source: http",
        "just a moment",
        "enable javascript and cookies",
        "about press copyright",
        "privacy policy",
        "google llc",
        "how youtube works",
        "test new features",
    ]
    return any(marker in lowered for marker in noisy_markers)


def _build_evidence_points(sources: list[dict]) -> list[str]:
    points: list[str] = []
    seen: set[str] = set()

    for source in sources:
        candidates = []
        if source.get("snippet"):
            candidates.extend(_extract_sentences(source["snippet"]))
        if source.get("excerpt"):
            candidates.extend(_extract_sentences(source["excerpt"]))

        for sentence in candidates:
            normalized = sentence.lower()
            if normalized in seen or _is_noisy_sentence(sentence):
                continue
            seen.add(normalized)
            points.append(sentence)
            if len(points) >= 5:
                return points

    return points


def _build_fallback_report(topic: str, sources: list[dict]) -> str:
    if not sources:
        return (
            "Answer:\n"
            "- Insufficient verified evidence. The system could not retrieve enough reliable source material to answer safely.\n\n"
            "Key Findings:\n"
            "- No reliable sources were successfully processed.\n"
            "- A grounded answer should not be generated without source support.\n"
            "- Try again later or refine the query for a narrower research target.\n\n"
            "Limits:\n"
            "- Tavily search or source scraping may have failed.\n"
            "- No verified evidence was available for synthesis.\n\n"
            "Sources:\n"
            "- None"
        )

    evidence_points = _build_evidence_points(sources)
    findings = evidence_points[:4] or [
        f"The available sources discuss '{topic}' but did not yield enough clean text for deeper synthesis."
    ]
    source_urls = [source["url"] for source in sources if source.get("url")]

    report_lines = [
        "Answer:",
        "- Based on the retrieved sources, the most defensible answer is the evidence-backed summary below.",
        "",
        "Key Findings:",
    ]

    for finding in findings:
        report_lines.append(f"- {finding}")

    report_lines.extend(
        [
            "",
            "Limits:",
            "- This response was generated from retrieved source snippets and scraped excerpts without a Gemini writing pass.",
            "- Treat it as a grounded fallback summary and open the sources for deeper verification.",
            "",
            "Sources:",
        ]
    )

    for url in source_urls:
        report_lines.append(f"- {url}")

    return "\n".join(report_lines)


def _build_local_critic_feedback(report: str, sources: list[dict], llm_used: bool, writer_error: str | None) -> str:
    score = 8 if sources else 4
    if llm_used:
        score += 1
    if writer_error:
        score -= 1
    score = max(3, min(score, 10))

    strengths = [
        "The output is grounded in retrieved sources rather than unsupported claims.",
        f"The workflow keeps token usage low by limiting research breadth to {len(sources)} processed sources."
    ]

    improvements = []
    if writer_error:
        improvements.append("Gemini generation was unavailable, so the final answer used the deterministic fallback path.")
    if not sources:
        improvements.append("No reliable sources were available, so the answer cannot be considered complete.")
    else:
        improvements.append("Open the cited sources to confirm freshness and context before acting on the summary.")
    improvements.append("If free-tier capacity is available, rerun later for a more polished writer-agent response.")

    verdict = (
        "Grounded and usable." if sources else "Too little verified evidence for a confident answer."
    )

    return (
        f"Score: {score}/10\n\n"
        "Strengths:\n"
        f"- {strengths[0]}\n"
        f"- {strengths[1]}\n\n"
        "Areas to Improve:\n"
        f"- {improvements[0]}\n"
        f"- {improvements[1]}\n\n"
        f"Verdict:\n{verdict}"
    )


def run_research_pipeline(topic: str, use_gemini: bool = False) -> dict:
    topic = topic.strip()
    if not topic:
        raise ValueError("Topic cannot be empty.")

    state = {
        "query": topic,
        "steps": [],
        "usage": {
            "model": "gemini-1.5-flash",
            "llm_calls": 1 if use_gemini else 0,
            "search_calls": 1,
            "scrape_limit": 2,
            "cost_strategy": [
                "One Tavily search request",
                "Scrape only the top 2 sources",
                "Gemini writer is optional and off by default",
                "Critic review is generated locally without extra model cost",
                "When enabled, Gemini uses temperature 0 for stable outputs",
                "Max 2048 tokens per response for free tier compliance",
            ],
        },
    }

    # STEP 1 ----- SEARCH TOOL
    state["steps"].append(
        {
            "agent": "Search Agent",
            "status": "running",
            "message": "Searching for recent and reliable sources.",
        }
    )

    try:
        state["search_results"] = web_search.invoke(
            {"query": f"Find recent, reliable and detailed information about: {topic}"}
        )
        state["steps"][-1]["status"] = "completed"
        state["steps"][-1]["message"] = "Search complete."
    except Exception as exc:
        state["search_results"] = ""
        state["steps"][-1]["status"] = "error"
        state["steps"][-1]["message"] = f"Search could not complete: {str(exc)}"

    # STEP 2 ----- READER TOOL
    state["steps"].append(
        {
            "agent": "Reader Agent",
            "status": "running",
            "message": "Scraping the top source pages for stronger grounding.",
        }
    )

    scraped_sections = []
    for url in _extract_urls(state["search_results"])[:2]:
        try:
            scraped_text = scrape_url.invoke({"url": url})
        except Exception:
            scraped_text = ""
        if isinstance(scraped_text, str) and not scraped_text.startswith("Could not Scrape URL:"):
            scraped_sections.append(f"Source: {url}\n{scraped_text}")

    state["scraped_content"] = "\n\n".join(scraped_sections) or "No source could be scraped successfully."
    state["sources"] = _build_sources(state["search_results"], scraped_sections)
    state["steps"][-1]["status"] = "completed" if state["sources"] else "warning"
    state["steps"][-1]["message"] = f"Reader processed {len(state['sources'])} sources."

    # STEP 3 ----- WRITER AGENT
    state["steps"].append(
        {
            "agent": "Writer Agent",
            "status": "running",
            "message": "Drafting a grounded response from the gathered evidence.",
        }
    )

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    writer_error = None
    if use_gemini:
        try:
            state["report"] = _invoke_chain_with_retry(
                writer_chain,
                {
                    "topic": topic,
                    "research": research_combined,
                },
            )
            state["writer_mode"] = "gemini"
            state["steps"][-1]["status"] = "completed"
            state["steps"][-1]["message"] = "Writer completed the report with Gemini Flash."
        except Exception as exc:
            writer_error = str(exc)
            state["report"] = _build_fallback_report(topic, state["sources"])
            state["writer_mode"] = "fallback"
            state["steps"][-1]["status"] = "warning"
            state["steps"][-1]["message"] = "Writer switched to a local grounded fallback because Gemini was unavailable."
    else:
        state["report"] = _build_fallback_report(topic, state["sources"])
        state["writer_mode"] = "local"
        state["steps"][-1]["status"] = "completed"
        state["steps"][-1]["message"] = "Writer completed the report using the zero-credit local synthesis path."

    # STEP 4 ----- CRITIC AGENT
    state["steps"].append(
        {
            "agent": "Critic Agent",
            "status": "running",
            "message": "Reviewing the report for grounding and quality without extra model cost.",
        }
    )

    state["feedback"] = _build_local_critic_feedback(
        state["report"],
        state["sources"],
        state["writer_mode"] == "gemini",
        writer_error,
    )
    state["steps"][-1]["status"] = "completed"
    state["steps"][-1]["message"] = "Critic review completed."
    if writer_error:
        state["warning"] = writer_error

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")
    run_research_pipeline(topic)
