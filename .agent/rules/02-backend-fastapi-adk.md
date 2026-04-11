---
trigger: always_on
description: Backend Standards (FastAPI & Google ADK)
---

# Backend: FastAPI & Google ADK

- **Tool Definitions:** Every ADK tool must have a clear, comprehensive docstring; this is the LLM's primary source of truth for function calling.
- **Type Safety:** Use Pydantic V2 models for all FastAPI request and response bodies, as well as ADK tool arguments.
- **Async First:** Use `async def` for FastAPI endpoints and I/O-bound ADK tool executions to prevent blocking the event loop.
- **Error Handling:** Use `fastapi.HTTPException` for client-side and tool-calling errors so the frontend GUI and the Agent can parse the status code and error details properly.