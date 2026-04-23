import os

from google import genai
from google.adk.agents import Agent
from ...config import config
from .prompt import VISUALIZATION_AGENT_PROMPT
from .tools import execute_visualization_code, execute_matplotlib_code

visualization_agent = Agent(
    model=config.BASE_MODEL,
    name="visualization_agent",
    description="Agent specialized in creating interactive and static visualizations.",
    instruction=VISUALIZATION_AGENT_PROMPT,
    tools=[execute_visualization_code, execute_matplotlib_code],
    generate_content_config=genai.types.GenerateContentConfig(
        max_output_tokens=config.VISUALIZATION_AGENT_MAX_OUTPUT_TOKENS,
    ),
)
