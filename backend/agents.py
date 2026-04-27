import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables FIRST from the .env file in the same directory
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

try:
    from tools import web_search, scrape_url
except ImportError:
    from .tools import web_search, scrape_url


# model setup
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("Missing GEMINI_API_KEY. Add it to your environment before running the project.")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    google_api_key=gemini_api_key,
    max_tokens=2048,
)

# Note: Tools (web_search, scrape_url) are invoked directly in pipeline.py
# No separate agent executors needed for free tier optimization

#WRITER CHAIN
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are the writer agent in a multi-agent research system. "
        "Use only the supplied research. Do not invent facts. "
        "If evidence is missing, say 'Insufficient verified evidence'. "
        "Keep the answer concise, practical, and grounded in the sources."
    ),
    (
        "human",
        """User query: {topic}

Verified research:
{research}

Write a source-grounded final answer in this exact structure:

Answer:
- Give the direct answer to the user's query.

Key Findings:
- 3 to 5 short, factual bullet points based only on the research.

Limits:
- Mention missing evidence, ambiguity, or freshness limits if relevant.

Sources:
- List only the URLs that appear in the research.
"""
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()

#CRITIC_CHAIN for critics
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are the critic agent in a multi-agent research system. "
        "Check whether the report is clear, grounded, and careful about uncertainty."
    ),
    (
        "human",
        """Review the report below.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

Verdict:
...
"""
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()
