# w_tools_agent

An ADK coding agent that uses a **manually defined Python tool** (`local_python_executor`) instead of ADK's built-in code executor. This is useful when you need full control over how generated code is executed, captured, or preprocessed.

## How It Works

1. The user sends a natural language request.
2. `qwen3-coder:30b` (via Ollama + LiteLLM) decides to call the `local_python_executor` tool with Python code as its argument.
3. The tool runs `exec()` locally, captures `stdout` via `io.StringIO`, and returns the output string to the agent.
4. The agent uses the output to formulate a final answer.

This is architecturally different from the other agents: the LLM explicitly **calls a tool** rather than outputting a fenced code block that ADK auto-executes.

### Key Files

| File | Purpose |
|---|---|
| [`agent.py`](./agent.py) | Defines the `root_agent` — wires the model and `local_python_executor` tool |
| [`tools.py`](./tools.py) | Implements `local_python_executor(code: str) -> str` |
| [`main.py`](./main.py) | FastAPI/uvicorn entry point for production / Cloud Run deployment |

### `local_python_executor` Tool

```python
def local_python_executor(code: str) -> str:
    """
    Executes Python code and returns the printed output.
    Use this for math, data analysis, or logic.
    """
```

The tool captures all `print()` output and returns it as a string. Exceptions are caught and returned as `"Error: ..."`.

## ⚠️ Safety Warning

> This tool uses `exec()` with no sandboxing. Only use for trusted, local workloads.

## Prerequisites

- Python `>=3.14`
- `uv` installed
- Ollama running at `http://localhost:11434` with `gemma4:26b` pulled:
  ```bash
  ollama pull gemma4:26b
  ```

## Running

### ADK Web UI (recommended)

From the project root (`ollama-adk-samples/`):

```bash
uv run adk web coder_agents
```

Open **http://localhost:8000** and select **`w_tools_agent`** from the dropdown menu.

### FastAPI / uvicorn server

For a production-style deployment (or Cloud Run), use `main.py`:

```bash
uv run uvicorn coder_agents.w_tools_agent.main:app --host 0.0.0.0 --port 8080
```

### REST API

Once the FastAPI server is running, you can interact via curl:

```bash
# Create a session
curl -X POST http://0.0.0.0:8080/apps/w_tools_agent/users/user_123/sessions/session_abc \
    -H "Content-Type: application/json" \
    -d '{"preferred_language": "English"}'

# Send a message
curl -X POST http://0.0.0.0:8080/run_sse \
    -H "Content-Type: application/json" \
    -d '{
    "app_name": "w_tools_agent",
    "user_id": "user_123",
    "session_id": "session_abc",
    "new_message": {
        "role": "user",
        "parts": [{"text": "What is 2 + 2? Verify with code."}]
    },
    "streaming": false
    }'
```

## Example Prompts

- `"What is 1234 * 5678? Use local_python_executor to verify."`
- `"Sort the list [5, 2, 9, 1, 7] and print each step."`
