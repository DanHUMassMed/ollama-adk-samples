import asyncio
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from financial_advisor.sub_agents.data_analyst.agent import data_analyst_agent

async def test_data_analyst():
    print("Testing data_analyst_agent with hooks applied...")
    runner = InMemoryRunner(agent=data_analyst_agent, app_name="test_app")
    session = await runner.session_service.create_session(app_name="test_app", user_id="user1", session_id="sess1")
    
    content = types.Content(role='user', parts=[types.Part(text="Can you look up Alphabet Q1 2026 earnings?")])
    events = runner.run_async(user_id="user1", session_id="sess1", new_message=content)
    
    final_output = ""
    async for event in events:
        if event.is_final_response() and event.content.parts:
            final_output = event.content.parts[0].text
            print("\nFINAL CLEANED RESPONSE:\n----------------")
            print(final_output)

if __name__ == "__main__":
    asyncio.run(test_data_analyst())
