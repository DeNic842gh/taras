# FastAPI Project Template

Scalable FastAPI starter with Poetry, layered structure (`api`, `core`, `schemas`), versioned routes, and settings via environment variables.

## Requirements

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)

## Quick start

```powershell
cd c:\Users\Denis\Desktop\taras
poetry install
poetry run serve
```

API: http://127.0.0.1:8000  
Docs: http://127.0.0.1:8000/docs  
Health: http://127.0.0.1:8000/api/v1/health

Copy `.env.example` to `.env` and adjust values as needed.

## Project layout

```
src/fastapi_project/
├── main.py              # App factory & entrypoint
├── api/v1/              # Versioned API routers
├── core/config.py       # Settings (pydantic-settings)
└── schemas/             # Pydantic models
tests/                   # Pytest suite
```

## Commands

| Command | Description |
|---------|-------------|
| `poetry run serve` | Start dev server with reload |
| `poetry run pytest` | Run tests |
| `poetry run ruff check src tests` | Lint |

## Git branches (Lab 1)

See [docs/LAB_GIT.md](docs/LAB_GIT.md) for creating the GitHub repo, `dev` / `main` branches, and the `git_logs.txt` file on `dev`.
