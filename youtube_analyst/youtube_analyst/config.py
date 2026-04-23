import os
from dataclasses import dataclass
from pydantic import Field
from typing import Any, Dict

from google.adk.models.lite_llm import LiteLlm

class WebSafeLiteLlm(LiteLlm):
    """
    Subclass of LiteLlm that prevents the ADK Web UI from crashing 
    without breaking the internal model execution.
    """
    
    def __init__(self, model: str, api_base: str | None = None, api_key: str | None = None, **kwargs):
        if api_base is not None:
            kwargs["api_base"] = api_base
        if api_key is not None:
            kwargs["api_key"] = api_key
        super().__init__(model=model, **kwargs)

    def model_dump(self, *args, **kwargs) -> Dict[str, Any]:
        """Ensures the Web UI gets a clean dictionary without internal objects."""
        # 1. Capture the existing exclusion list
        exclude = kwargs.get("exclude", set())
        
        # 2. Add 'llm_client' to the exclusion set so FastAPI ignores it
        if isinstance(exclude, set):
            exclude.add("llm_client")
        elif isinstance(exclude, dict):
            exclude["llm_client"] = True
        
        kwargs["exclude"] = exclude
        
        # 3. Call the parent dump with the new exclusions
        return super().model_dump(*args, **kwargs)

# --- 2. Use the Wrapper in your Config ---
@dataclass
class AgentConfiguration:
    """Configuration for agents models and parameters."""
    YOUTUBE_SEARCH_API = os.getenv("YOUTUBE_SEARCH_API")
    YOUTUBE_AGENT_MAX_OUTPUT_TOKENS = 8000
    VISUALIZATION_AGENT_MAX_OUTPUT_TOKENS = 30000
    GOOGLE_GENAI_LOCATION = "global"

    # Swap 'LiteLlm' for 'WebSafeLiteLlm'
    BASE_MODEL = WebSafeLiteLlm(
        model="openai/gemma4:26b",
        api_base="http://localhost:11434/v1",
        api_key="no_ollama_key_needed",
    )

    DEEP_MODEL = WebSafeLiteLlm(
        model="openai/gemma4:31b",
        api_base="http://localhost:11434/v1",
        api_key="no_ollama_key_needed",
    )

    FAST_MODEL = BASE_MODEL

config = AgentConfiguration()