import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns titles, URLs and snippets."""
    results = tavily.search(query=query, max_results=6)

    out = []
    for result in results["results"]:
        url = result["url"]
        if "youtube.com" in url or "youtu.be" in url:
            continue
        out.append(
            f"Title: {result['title']}\n"
            f"URL: {url}\n"
            f"Snippet: {result['content'][:300]}\n"
        )
        if len(out) == 3:
            break
    return "\n----\n".join(out)


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        for tag in soup(["script", "style", "nav", "footer", "meta", "link"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)[:2500]
        return text if text.strip() else "Could not Scrape URL:Empty content"
    except requests.exceptions.Timeout:
        return "Could not Scrape URL:Timeout (site too slow)"
    except requests.exceptions.ConnectionError:
        return "Could not Scrape URL:Connection error"
    except Exception as exc:
        return f"Could not Scrape URL:{str(exc)[:50]}"
