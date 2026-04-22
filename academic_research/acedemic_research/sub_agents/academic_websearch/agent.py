
from google.adk import Agent
from google.adk.tools import MCPToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from mcp import StdioServerParameters
from . import prompt
from ...config import config

from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
SEARXNG_SERVER_PATH = CURRENT_DIR / "searxng_mcp" / "server.py"

academic_websearch_agent = Agent(
    name="academic_websearch_agent",
    model=config.BASE_MODEL,
    instruction=prompt.ACADEMIC_WEBSEARCH_PROMPT,
    output_key="recent_citing_papers",
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uv",
                    args=["run", str(SEARXNG_SERVER_PATH)],
                ),
            ),
        )
    ],
)


