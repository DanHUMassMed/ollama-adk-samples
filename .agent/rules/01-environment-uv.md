---
description: Environment Management (uv)
---
# Environment Management (uv)

- ALWAYS use `uv` for package management and script execution. Do not use standard `pip` or `pipenv`.
- **Lockfile:** Do not manually edit `pyproject.toml` dependencies without running `uv lock` or `uv add`.
- **In-Project Venv:** Assume the active virtual environment is located at `.venv`.
- **Execution:** Prefer `uv run <cmd>` for scripts to ensure the correct environment state is used.
- **Syncing:** If a module is missing or throwing an ImportError, run `uv sync` before attempting to troubleshoot the code itself.
