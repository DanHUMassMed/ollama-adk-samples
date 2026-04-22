
from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
from . import prompt
from ...callbacks import strip_thinking_hook

MODEL=LiteLlm(model="openai/gemma4:26b",
            api_base="http://localhost:11434/v1", 
            api_key="my_api_key")

trading_analyst_agent = Agent(
    model=MODEL,
    name="trading_analyst_agent",
    instruction=prompt.TRADING_ANALYST_PROMPT,
    output_key="proposed_trading_strategies_output",
    after_model_callback=strip_thinking_hook,
)
