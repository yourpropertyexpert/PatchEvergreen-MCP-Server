from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("PEG")

@mcp.tool()
def get_issues_for_library(library: str, language: str) -> dict:
    """Fetch issues for a given library and language from PatchEvergreen API."""
    url = "https://app.patchevergreen.com/api/getissuesforlibrary.php"
    params = {"library": library, "language": language}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

mcp.run(transport="sse")
