import re
from typing import Optional
from copy import deepcopy
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_response import LlmResponse
from google.genai import types 

def strip_thinking_hook(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    """Intercepts LLM response and strips out parts marked as thought."""
    if not llm_response.content or not llm_response.content.parts:
        return None
        
    modified_parts = []
    has_changes = False
    
    for i, part in enumerate(llm_response.content.parts):
        # The user requested to print the text so we see the output while it is processing
        # if hasattr(part, 'text') and part.text:
        #    print(f"--- Part {i} --- thought={getattr(part, 'thought', False)}\n{part.text}\n")
        
        # Check if it has a thought attribute
        is_thought = getattr(part, 'thought', False)
        
        # Also check dict access just in case the SDK parsed it to a dict internally
        if isinstance(part, dict) and part.get('thought', False):
            is_thought = True

        if is_thought:
            has_changes = True
            # print(f"DEBUG: Stripping thought part: {part.text[:50] if hasattr(part, 'text') else '...'}...")
        else:
            modified_parts.append(deepcopy(part))
            
    if has_changes:
        return LlmResponse(
             content=types.Content(role="model", parts=modified_parts),
             grounding_metadata=llm_response.grounding_metadata
        )
    
    return None

def enforce_think_tags(original_prompt: str) -> str:
    """Pass-through: Gemma4 handles thoughts natively, no prompt enforcing needed."""
    return original_prompt
