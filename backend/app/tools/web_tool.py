# ============================================================
#  Zarix AgentOS — Web Search & Fetch Tool
# ============================================================
from __future__ import annotations

import asyncio
import logging

import httpx
from bs4 import BeautifulSoup

from app.core.config import settings
from app.tools.base import BaseTool, ToolResult

logger = logging.getLogger(__name__)


class WebSearchTool(BaseTool):
    """Search the web and return results (uses DuckDuckGo HTML endpoint)."""

    name = "web_search"
    description = (
        "Search the web for information. Returns a list of results with "
        "title, URL, and snippet."
    )
    category = "web"

    SEARCH_URL = "https://html.duckduckgo.com/html/"

    async def execute(self, query: str, max_results: int = 5, **kwargs) -> ToolResult:
        if not settings.enable_web_search:
            return ToolResult(success=False, error="Web search is disabled")

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    self.SEARCH_URL,
                    data={"q": query},
                    headers={
                        "User-Agent": "Mozilla/5.0 (compatible; ZarixAgentOS/1.0)"
                    },
                )
                resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")
            results = []
            for item in soup.select(".result"):
                title_el = item.select_one(".result__title")
                link_el = item.select_one(".result__url")
                snippet_el = item.select_one(".result__snippet")
                if title_el:
                    results.append(
                        {
                            "title": title_el.get_text(strip=True),
                            "url": (link_el.get_text(strip=True) if link_el else ""),
                            "snippet": (
                                snippet_el.get_text(strip=True)
                                if snippet_el
                                else ""
                            ),
                        }
                    )
                if len(results) >= max_results:
                    break

            return ToolResult(
                success=True,
                output=f"Found {len(results)} results for '{query}'",
                data={"results": results},
            )

        except Exception as exc:
            logger.error("Web search failed: %s", exc)
            return ToolResult(success=False, error=str(exc))


class WebFetchTool(BaseTool):
    """Fetch the content of a web page and extract text."""

    name = "web_fetch"
    description = (
        "Fetch a URL and return the page text content, stripped of HTML."
    )
    category = "web"

    async def execute(self, url: str, max_chars: int = 5000, **kwargs) -> ToolResult:
        try:
            async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
                resp = await client.get(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (compatible; ZarixAgentOS/1.0)"
                    },
                )
                resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")
            # Remove script/style elements
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            text = soup.get_text(separator="\n", strip=True)
            text = text[:max_chars]

            return ToolResult(
                success=True,
                output=text,
                data={"url": url, "title": soup.title.string if soup.title else ""},
            )

        except Exception as exc:
            logger.error("Web fetch failed: %s", exc)
            return ToolResult(success=False, error=str(exc))
