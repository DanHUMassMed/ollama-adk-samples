import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import MCPToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from mcp import StdioServerParameters


MODEL=LiteLlm(model="openai/gemma4:26b",
                api_base="http://localhost:11434/v1", 
                api_key="my_api_key"
                )

root_agent = Agent(
    name="searngx_search_agent",
    model=MODEL,
    description=(
        "Search agent for finding current information, news, headlines, and web content."
    ),
    instruction=(
        "You are a search tool wrapper. You do not have knowledge of current events. "
        "Therefore, you MUST ALWAYS use the search tool for ANY query the user provides, including requests for news, today's headlines, or current events. "
        "Do not answer from your own knowledge or refuse the prompt. IMMEDIATELY call the search tool using the user's prompt as the query. "
        "Return the search tool's results as a formatted Markdown list without any conversational filler.\n\n"
        "--- EXAMPLES ---\n"
        "User: \"What are today's headlines?\"\n"
        "[You must invoke the search tool with the query: \"today's headlines\"]\n"
        "\n"
        "User: \"Latest AI news\"\n"
        "[You must invoke the search tool with the query: \"Latest AI news\"]\n"
    ),
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uv",
                    args=["run", "searxng_mcp/server.py"],
                ),
            ),
        )
    ],
)
