# container_agent

An ADK coding agent that executes LLM-generated Python code inside an **isolated Docker container** using ADK's built-in `ContainerCodeExecutor`. It uses the standard `python:3.11-slim` image with configurable memory and CPU limits.

## How It Works

1. The user sends a natural language request.
2. `gemini-3-flash-preview` generates Python code in a fenced markdown block.
3. ADK's `ContainerCodeExecutor` spins up (or reuses) a `python:3.11-slim` Docker container with the configured resource limits.
4. The code is injected and executed inside the container.
5. Stdout is returned to the agent and presented to the user.

**Source:** [`agent.py`](./agent.py)

```python
local_python_executor = ContainerCodeExecutor(
    image="python:3.11-slim",
    timeout=10,          # max execution time in seconds
    memory_limit="256m", # memory cap
    cpu_limit=1.0        # CPU limit
)
```

> **Note:** `container_agent` now uses `gemma4:26b` via Ollama + LiteLLM (same as all other coder agents).

## Prerequisites

- Python `>=3.14`
- `uv` installed
- **Docker** installed and running
  - [Install Docker Desktop](https://docs.docker.com/get-docker/) (Mac/Windows)
  - Verify: `docker info`
- The `python:3.11-slim` image pulled (Docker will auto-pull if missing):
  ```bash
  docker pull python:3.11-slim
  ```
- Ollama running at `http://localhost:11434` with `gemma4:26b` pulled:
  ```bash
  ollama pull gemma4:26b
  ```

## Running

From the project root (`ollama-adk-samples/`):

```bash
uv run adk web coder_agents
```

Open **http://localhost:8000** and select **`container_agent`** from the dropdown menu.

## Resource Limits

| Parameter | Value | Purpose |
|---|---|---|
| `image` | `python:3.11-slim` | Minimal Python runtime |
| `timeout` | `10s` | Prevents infinite loops |
| `memory_limit` | `256m` | Prevents memory exhaustion |
| `cpu_limit` | `1.0` | Caps CPU usage to 1 core |

## Caveats

- **Network from inside container:** Code running inside the container cannot reach `localhost:11434` (Ollama). Use `host.docker.internal` instead on Mac/Windows if needed.
- **No extra packages:** `python:3.11-slim` has only the stdlib. The LLM cannot use `numpy`, `pandas`, etc. unless it `pip install`s them at runtime (which adds latency).
- **Cold start:** First execution will pull the Docker image if not cached.

## Example Prompts

- `"What is the square root of 144? Verify with Python."`
- `"Write code to check if 997 is a prime number."`
