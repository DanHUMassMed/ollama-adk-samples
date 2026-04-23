from dataclasses import dataclass

from google.adk.models.lite_llm import LiteLlm

# import litellm
# litellm._turn_on_debug()

@dataclass
class AgentConfiguration:
    """Configuration for agents models and parameters."""

    BASE_MODEL = LiteLlm(
        model="openai/gemma4:26b",
        api_base="http://localhost:11434/v1",
        api_key="no_ollama_key_needed",
    )

    DEEP_MODEL = LiteLlm(
        model="openai/gemma4:31b",
        api_base="http://localhost:11434/v1",
        api_key="no_ollama_key_needed",
    )

    FAST_MODEL = BASE_MODEL

config = AgentConfiguration()
