# RAG Evaluations

This directory contains scripts to evaluate the RAG Agent against testing datasets. The tests are written using `pytest` and utilize Python's `asyncio` integration for non-blocking agent evaluations.

## Generating the EvalSet Data

You may notice two JSON files in the `data/` directory:
- `conversation.test.1.json`
- `conversation.test.1.evalset.json`

While the `.evalset.json` file looks like a complex, serialized session capture—it is actually a generated artifact. The `google-adk` v2 framework requires a robust runtime schema (`EvalSet`) for evaluations.

Instead of writing the complex session state manually, you only need to write the **human-readable** test cases containing the `query`, `expected_tool_use`, and `reference` inside `conversation.test.1.json`.

Then, you compile it into the framework's format using the provided `migrate_eval_data.py` script:

```bash
uv run python RAG/eval/migrate_eval_data.py
```

This script invokes `AgentEvaluator.migrate_eval_data_to_new_schema()` to automatically convert your simplified JSON test definitions into the rigorous `.evalset.json` format used by the test runner.

## Running the Tests

Because the `adk` tests run via the Python test framework and require your virtual environment dependencies, you must use `uv run` alongside `pytest`.

To execute the test script from your workspace root (e.g., `ollama-adk-samples`), run the following command in your terminal:

```bash
uv run pytest RAG/eval/test_eval.py -v
```

### Explanation of the Command
- `uv run` ensures the test is strictly executed within the virtual environment correctly resolving any required pip packages (like `google-adk`, `pytest`, `pytest-asyncio`).
- `pytest` automatically sweeps the Python file to identify your `@pytest.mark.asyncio` labeled function `test_eval_full_conversation` and runs it.
- `-v` is the verbose flag to give you more detailed tracing of passed/failed tests.

### Required Dependencies
This approach relies on the `pytest` and `pytest-asyncio` plugins which have successfully been installed and resolved in the `pyproject.toml` workspace environment via `make dev` and `uv sync`.

## Running Phoenix-Instrumented Evaluations

In addition to the standard `google-adk` evaluation pipeline, this directory contains `test_eval_phoenix.py`. This is a **standalone custom evaluation script** designed to instrument your Agent's evaluation directly into your Arize Phoenix tracing view.

Unlike `test_eval.py` which employs an LLM judge to determine pass/fail criteria, `test_eval_phoenix.py` relies on lightweight python evaluator heuristic functions:
- `trajectory_exact_match_evaluator`: Validates sequence constraints securely.
- `trajectory_precision_evaluator`: Scores tool usage overlap and extra hallucinated tools.
- `tool_name_match_evaluator`: Scores pure tool coverage independent of counts or arguments.

Since it is a standalone `asyncio` script building pandas data frames, it bypasses the `pytest` runner. 

To run the custom evaluations:
1. Ensure your Phoenix UI dashboard is actively running in the background (e.g., via `make phoenix`).
2. Execute the python script directly inside the environment:
```bash
uv run python RAG/eval/test_eval_phoenix.py
```
The script will process your conversational tests, upload all context pairs into the Phoenix trace server under an `Eval` project label, and output an aggregated pandas DataFrame layout directly into your terminal.
