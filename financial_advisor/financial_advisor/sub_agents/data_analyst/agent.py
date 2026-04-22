
"""data_analyst_agent for finding information using searxng search"""

from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
from .tools import searxng_search_tool

from . import prompt
from ...callbacks import strip_thinking_hook

MODEL=LiteLlm(model="openai/gemma4:26b",
            api_base="http://localhost:11434/v1", 
            api_key="my_api_key")

data_analyst_agent = Agent(
    model=MODEL,
    name="data_analyst_agent",
    instruction=prompt.DATA_ANALYST_PROMPT,
    output_key="market_data_analysis_output",
    tools=[searxng_search_tool],
    after_model_callback=strip_thinking_hook,
)
