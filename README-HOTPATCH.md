# OpenInference ADK Instrumentation Hot-Patch

## The Bug
The `google-adk` package version `2.0.0a3` contains a prerelease version string (`"a3"`).
The upstream tracking plugin `openinference-instrumentation-google-adk` (up to v0.1.10) naively attempts to cast the components of this version string strictly as `int()`.
As a result, launching the `adk web` agent server with Phoenix tracing enabled crashes with the following error:
```
ValueError: invalid literal for int() with base 10: '0a3'
```

## The Solution
We have provided an automated python script `patch_openinference.py` that will comb through your local virtual environment cache (`.venv/lib/python-*/site-packages/...`), locate the buggy line in `openinference/instrumentation/google_adk/__init__.py`, and selectively replace the `int(x)` evaluator with a safeguard that strips prerelease alphanumeric characters before checking package bounds.

### How to use
If you ever purge, blow away, or rebuild your `.venv` environment (e.g. by running a fresh `uv sync` from scratch), the bug will resurface until `openinference` publishes a fix on PyPI.

If that happens, you can simply run:

```bash
uv run python patch_openinference.py
```

This will automatically locate the instrumentation folder and patch the schema directly. Then your server should launch cleanly again!
