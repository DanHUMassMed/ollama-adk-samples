import asyncio
import os
from google.adk.models.lite_llm import LiteLlm
from google.adk.models import LlmRequest
from google.genai import types
import re

MODEL=LiteLlm(model="openai/qwen3.6:35b",
            api_base="http://localhost:11434/v1", 
            api_key="my_api_key")

async def test_llm():
    req = LlmRequest(
        contents=[
            types.Content(
                role="user",
                parts=[types.Part(text="Think step by step and tell me what 2 + 2 is.")]
            )
        ],
        config=types.GenerateContentConfig(
            system_instruction=types.Content(role="system", parts=[types.Part(text="You must place all of your internal reasoning and thinking step-by-step inside `<think>...</think>` tags. Your final answer should be placed after the tags.")])
        )
    )
    res_gen = MODEL.generate_content_async(req)
    final_output = []
    async for chunk in res_gen:
        for part in getattr(chunk.content, 'parts', []):
            if part.text:
                final_output.append(part.text)
    full_text = "".join(final_output)
    print("FULL TEXT:\n", full_text)
    
    # test stripping
    stripped = re.sub(r'<think>.*?</think>', '', full_text, flags=re.DOTALL)
    print("\nSTRIPPED OUTPUT:\n", stripped.strip())

if __name__ == "__main__":
    asyncio.run(test_llm())
