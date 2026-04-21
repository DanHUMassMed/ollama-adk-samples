# Coder Agents

A collection of Google ADK coding agents demonstrating **four different code execution strategies**, from completely unsafe local execution up to fully Docker-sandboxed environments. Each sub-agent is runnable independently via the ADK web UI.

## Architecture Overview

All agents share the same pattern — an `LlmAgent` that generates Python code and a `code_executor` (or tool) that actually runs it. The key difference between variants is **where and how** the generated code executes:

```
┌────────────────────────────────────────────────────┐
│                  User Prompt                       │
│          "Calculate the Sharpe ratio…"             │
└────────────────────────┬───────────────────────────┘
                         │
                    LLM (via LiteLLM / Ollama)
                         │
              generates Python code block
                         │
          ┌──────────────▼──────────────┐
          │     Code Executor / Tool    │
          └──────────────┬──────────────┘
                         │
        ┌────────────────┼──────────────────────┐
        ▼                ▼                       ▼
  unsafe_agent    container_agent /       w_tools_agent
  (exec() locally) sandbox_agent           (custom tool)
                  (Docker container)
```

## Sub-agents

| Directory | Execution Strategy | Safety | Docker Required |
|---|---|---|---|
| [`unsafe_agent/`](./unsafe_agent/) | `UnsafeLocalCodeExecutor` | ❌ No sandbox | No |
| [`w_tools_agent/`](./w_tools_agent/) | Custom `exec()`-based tool | ⚠️ No isolation | No |
| [`container_agent/`](./container_agent/) | `ContainerCodeExecutor` with `python:3.11-slim` | ✅ Isolated | Yes |
| [`sandbox_agent/`](./sandbox_agent/) | `ContainerCodeExecutor` with custom `docker-sandbox` image | ✅ Isolated + scientific stack | Yes |

> All agents use **`gemma4:26b`** via Ollama + LiteLLM.

## Prerequisites

- Python `>=3.14`
- [`uv`](https://docs.astral.sh/uv/) for package management
- [Ollama](https://ollama.com) running locally at `http://localhost:11434`
- Required model pulled:
  ```bash
  ollama pull gemma4:26b
  ```
- Docker (only for `container_agent` and `sandbox_agent`)

## Quick Start

Run **all four agents at once** from the project root (`ollama-adk-samples/`) with a single command:

```bash
uv run adk web coder_agents
```

Then open **http://localhost:8000** — all agents appear in the **dropdown menu** in the top-left corner of the UI. No need to stop and restart the server to switch between them.

---

See each sub-directory's `README.md` for agent-specific setup and caveats.
