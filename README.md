# FastAPI Project

Production-ready layout with Poetry, Docker, PostgreSQL, and Alembic.

## Structure

```
app/
├── main.py              # Entry point (app = FastAPI())
├── core/                # config, security, exceptions
├── api/v1/endpoints/    # auth, users, posts, health
├── crud/                # Database operations
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── db/                  # session, base (Alembic metadata)
└── utils/               # helpers (email, etc.)
tests/
alembic/                 # DB migrations
```

## Local development

```powershell
poetry install
copy .env.example .env
poetry run serve
```

- Docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/api/v1/health

## Migrations

```powershell
poetry run alembic revision --autogenerate -m "init"
poetry run alembic upgrade head
```

## Docker (2 containers: API + PostgreSQL)

**Production:**

```powershell
docker compose up -d --build
```

**Development** (`--reload` + volume `.:/app`):

```powershell
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
```

See [docs/LAB2.md](docs/LAB2.md).
