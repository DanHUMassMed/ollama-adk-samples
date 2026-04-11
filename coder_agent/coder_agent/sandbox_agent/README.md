# Sandbox Agent

This directory contains `sandbox_agent`, an agent that uses the `ContainerCodeExecutor` to run Python code securely within a Docker container.

## Requirements

The `ContainerCodeExecutor` requires Docker to be installed and running on your host machine.

1. **Install Docker**: Download and install Docker Desktop (or Docker Engine) from [docker.com](https://docs.docker.com/get-docker/).
2. **Start Docker**: Make sure the Docker daemon is running before executing this agent.
3. **Docker Image**: By default, the `ContainerCodeExecutor` may attempt to pull a Python image (e.g., `python:3.11-slim`) if one is not specified or not present locally.

## Execution Gotchas

- **Docker daemon permissions**: If you see errors about connecting to the Docker daemon, ensure your user has appropriate permissions to access the Docker socket (e.g., being in the `docker` group on Linux, or ensuring Docker Desktop is running properly on Mac/Windows).
- **Network Isolation**: By default, the container might have restricted or no network access to the host machine unless explicitly configured. If your agent's generated code needs to make web requests or connect to host services (like the LiteLLM server at `localhost:11434`), you may need to pass additional configuration to the `ContainerCodeExecutor` or ensure the host networking is accessible from within the container (e.g., using `host.docker.internal` on Mac/Windows).
- **Timeouts and Limitations**: Execution from the container is time and resource bound. If the code takes too long, it will be terminated.


#### Build the docker image with the below command
```
cd sandbox_agent/sandbox
docker build -t docker-sandbox .
```

