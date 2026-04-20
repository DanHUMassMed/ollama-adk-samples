VENV := .venv
PYTHON := $(VENV)/bin/python
RUFF := $(VENV)/bin/ruff
MYPY := $(VENV)/bin/mypy
UV := $(VENV)/bin/uv

.PHONY: dev lint run check-venv

check-venv:
	@test -x $(PYTHON) || (echo "❌ Virtualenv not found. Run: uv sync" && exit 1)

dev:
	uv sync --extra dev --prerelease allow

phoenix:
	PHOENIX_HOST=127.0.0.1 PHOENIX_PORT=8081 uv run phoenix serve

lint: check-venv
	$(RUFF) format retail_location_strategy/
	$(RUFF) check retail_location_strategy/
	$(MYPY) retail_location_strategy/

backend: check-venv
	uv run python -m retail_location_strategy.main

frontend: check-venv
	cd frontend;npm run dev

phoenix: check-venv
	uv run phoenix serve
