import httpx
from typing import List, Optional, Dict, Any

class SearXNGConnector:
    def __init__(self, base_url: str = "http://localhost:32768"):
        self.base_url = base_url.rstrip("/")

    async def search(
        self,
        query: str,
        categories: Optional[List[str]] = None,
        engines: Optional[List[str]] = None,
        language: str = "en",
        page: int = 1,
        time_range: Optional[str] = None,
        max_results: Optional[int] = None,
        timeout: float = 10.0,
    ) -> Dict[str, Any]:
        """
        Search SearXNG instance.
        
        Args:
            query: Search query string
            categories: List of categories to search (e.g., ['general', 'it'])
            engines: List of specific engines to use
            language: Language code (default: en)
            page: Page number (default: 1)
            time_range: Time range (e.g., 'day', 'week', 'month', 'year')
            max_results: Maximum number of results to return (optional)
            timeout: Request timeout in seconds (default: 10.0)
        """
        params = {
            "q": query,
            "format": "json",
            "language": language,
            "pageno": page,
        }

        if categories:
            params["categories"] = ",".join(categories)
        if engines:
            params["engines"] = ",".join(engines)
        if time_range:
            params["time_range"] = time_range

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            data = response.json()

        results = data.get("results", [])
        
        if max_results and len(results) > max_results:
            results = results[:max_results]
            
        return {
            "query": data.get("query"),
            "number_of_results": data.get("number_of_results"),
            "results": results,
            "suggestions": data.get("suggestions", []),
            "infoboxes": data.get("infoboxes", []),
        }


async def searxng_search_tool(query: str, max_results: int = 10) -> Dict[str, Any]:
    """Search the web using SearXNG.

    Args:
        query: Search query string
        results: Number of results to return (default: 10)
    """
    connector = SearXNGConnector()
    results = await connector.search(query=query, max_results=max_results)
    return results
