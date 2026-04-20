
from .prompts import return_instructions_root
from .tools import ask_chromadb
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from openinference.instrumentation import using_session
import uuid
from .tracing import instrument_adk_with_phoenix

# Monkey-patch LiteLlm schema to avoid Pydantic serialization errors on the API router
if 'llm_client' in LiteLlm.model_fields:
    LiteLlm.model_fields['llm_client'].exclude = True
    LiteLlm.model_rebuild(force=True)

# Run Phoenix UI: phoenix serve
try:
    _ = instrument_adk_with_phoenix()
except Exception as e:
    print(f"Tracing disabled due to error: {e}")



MODEL=LiteLlm(model="openai/gpt-oss:20b",
                api_base="http://localhost:11434/v1", 
                api_key="my_api_key"
                )

with using_session(session_id=str(uuid.uuid4())):
    root_agent = Agent(
        name="ask_rag_agent",
        model=MODEL,
    description="A simple agent that can answer questions based on documents.",
    instruction=return_instructions_root(),
    tools=[ask_chromadb],
)

print("✅ Root Agent defined.")


