# unsafe_agent

An ADK coding agent that uses `UnsafeLocalCodeExecutor` to run LLM-generated Python code **directly on the host machine** using Python's built-in `exec()`. This is the simplest possible setup — no Docker, no sandboxing.

## ⚠️ Safety Warning

> **This agent executes arbitrary code in your local Python process with no isolation.**  
> Only use this for trusted local experimentation. Never expose it to untrusted input or external networks.

## How It Works

1. The user sends a natural language coding request.
2. `qwen3-coder:30b` (via Ollama + LiteLLM) generates a Python code block.
3. ADK's `UnsafeLocalCodeExecutor` runs that code directly in the current Python process using `exec()`.
4. The stdout output is returned as the agent's response.

**Source:** [`agent.py`](./agent.py)

```python
root_agent = Agent(
    name="code_assistant",
    model=model,
    code_executor=UnsafeLocalCodeExecutor(),
    instruction="You are a coder. Create Python code to verify your math.",
)
```

## Prerequisites

- Python `>=3.14`
- `uv` installed
- Ollama running at `http://localhost:11434` with `gemma4:26b` pulled:
  ```bash
  ollama pull gemma4:26b
  ```

## Running

From the project root (`ollama-adk-samples/`):

```bash
uv run adk web coder_agents
```

Open **http://localhost:8000** and select **`unsafe_agent`** from the dropdown menu.

## Example Prompts

- `"What is 1234 * 5678? Verify with code."`
- `"Generate a list of the first 20 Fibonacci numbers."`
- `"Create a pandas DataFrame with 5 rows of random data and print the describe() stats."`

> **Note:** The agent needs `pandas`, `numpy`, etc. available in your local `.venv` for those libraries to work. Check `pyproject.toml` for what is installed.
