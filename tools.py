from langchain.tools import tool 
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os 
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""
    try:
        results = tavily.search(query=query, max_results=5)
        out = []
        for r in results.get('results', []):
            out.append(
                f"Title: {r.get('title', '')}\nURL: {r.get('url', '')}\nSnippet: {r.get('content', '')[:300]}\n"
            )
        return "\n----\n".join(out) if out else "No web results found for this query."
    except Exception as e:
        return f"Search encountered an issue: {str(e)}"

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "close"
        }
        resp = session.get(url, timeout=10, headers=headers, allow_redirects=True)
        if resp.status_code != 200:
            return f"Failed to access page (status code {resp.status_code})"
            
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "svg"]):
            tag.decompose()
            
        text = soup.get_text(separator=" ", strip=True)
        return text[:3000] if text else "Page content was empty or unparseable."
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"

