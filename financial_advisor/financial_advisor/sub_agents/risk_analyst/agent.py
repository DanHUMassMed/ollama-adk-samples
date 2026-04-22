"""Risk Analysis Agent for providing the final risk evaluation"""


from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
from . import prompt
from ...callbacks import strip_thinking_hook

MODEL=LiteLlm(model="openai/gemma4:26b",
            api_base="http://localhost:11434/v1", 
            api_key="my_api_key")

risk_analyst_agent = Agent(
    model=MODEL,
    name="risk_analyst_agent",
    instruction=prompt.RISK_ANALYST_PROMPT,
    output_key="final_risk_assessment_output",
    after_model_callback=strip_thinking_hook,
)
