# sandbox_agent

An ADK coding agent that executes LLM-generated Python code in a **custom Docker container** (`docker-sandbox`) pre-loaded with a full scientific computing stack (numpy, pandas, matplotlib, scikit-learn, etc.). This is the most capable and secure variant.

## How It Works

1. The user sends a natural language request.
2. `gemma4:26b` (via Ollama + LiteLLM) generates Python code.
3. ADK's `ContainerCodeExecutor` runs the code inside the `docker-sandbox` container.
4. The container provides full access to numpy, pandas, matplotlib, scipy, scikit-learn, statsmodels, plotly, and pyarrow.
5. Output is returned to the agent.

**Source:** [`agent.py`](./agent.py)

```python
root_agent = Agent(
    name="code_assistant",
    model=model,
    code_executor=ContainerCodeExecutor(image="docker-sandbox"),
    instruction="You are a coder. Create Python code to verify your math. if required do pip inst",
)
```

## Docker Image: `docker-sandbox`

The custom image is defined in [`sandbox/dockerfile`](./sandbox/dockerfile). It is based on `python:3.13.12-trixie` and includes:

| Package | Purpose |
|---|---|
| `numpy` | Numerical computing |
| `pandas` | Data analysis and DataFrames |
| `matplotlib` + `seaborn` | Plotting (non-interactive, `Agg` backend) |
| `scipy` | Scientific computing |
| `scikit-learn` | Machine learning |
| `statsmodels` | Statistical models |
| `plotly` | Interactive visualizations |
| `pyarrow` | columnar data / Parquet I/O |

## Prerequisites

- Python `>=3.14`
- `uv` installed
- **Docker** installed and running — [Install Docker](https://docs.docker.com/get-docker/)
- Ollama running at `http://localhost:11434` with `gemma4:26b` pulled:
  ```bash
  ollama pull gemma4:26b
  ```

## Setup: Build the Docker Image

You must build the `docker-sandbox` image **before** running the agent. From the project root:

```bash
cd coder_agents/sandbox_agent/sandbox
docker build -t docker-sandbox .
```

This only needs to be done once (or whenever the Dockerfile changes).

## Running

From the project root (`ollama-adk-samples/`):

```bash
uv run adk web coder_agents
```

Open **http://localhost:8000** and select **`sandbox_agent`** from the dropdown menu.

## Caveats

- **Docker daemon permissions**: On Linux, ensure your user is in the `docker` group. On Mac/Windows, ensure Docker Desktop is running.
- **Network Isolation**: Code running inside the container cannot reach `localhost:11434` (Ollama). Use `host.docker.internal` instead on Mac/Windows if needed.
- **Matplotlib plots**: The `Agg` backend (`MPLBACKEND=Agg`) is set so matplotlib works headlessly. Use `plt.savefig()` rather than `plt.show()`.

## Example Prompts

- `"Fit a linear regression on x=[1,2,3,4,5] y=[2,4,5,4,5] and print the R² score."`
- `"Generate a 100-row DataFrame of random stock prices and plot a rolling 7-day average."`
- `"Run a K-means clustering on 200 random 2D points with k=3 and print the cluster centers."`

