---
description: Project Hierarchy and Organization
---
# Project Hierarchy

Maintain strict boundaries between the tool-calling backend and the UI:
- `backend/`: Contains FastAPI source code, ADK tool definitions, backend tests, and `pyproject.toml`.
- `frontend/`: Contains the Vite/React source, MUI theme configuration, and `package.json`.
- `shared/`: (Optional) Contains JSON schemas or type definitions shared between ADK tool definitions and frontend API clients (e.g., for form validation).
- **Imports:** Use absolute imports for backend modules (`from app.services...`) and aliased imports for frontend components (e.g., `@/components/...`).
