"""Execution_analyst_agent for finding the ideal execution strategy"""

from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
from . import prompt
from ...callbacks import strip_thinking_hook

MODEL=LiteLlm(model="openai/gemma4:26b",
            api_base="http://localhost:11434/v1", 
            api_key="my_api_key")

execution_analyst_agent = Agent(
    model=MODEL,
    name="execution_analyst_agent",
    instruction=prompt.EXECUTION_ANALYST_PROMPT,
    output_key="execution_plan_output",
    after_model_callback=strip_thinking_hook,
)
