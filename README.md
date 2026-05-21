# FastAPI Project — PostgreSQL (async)

Production-style FastAPI app with **async PostgreSQL**, SQLAlchemy 2 async, Alembic, and Pydantic Settings.

## Stack

- FastAPI + APIRouter
- SQLAlchemy Async + AsyncSession + asyncpg
- Alembic (async migrations, autogenerate)
- Pydantic Settings (`.env`)
- Poetry

## Project structure

```
app/
├── main.py              # FastAPI app factory
├── api/v1/endpoints/    # Routers (users, profiles, categories, products, posts, orders, order-items)
├── core/                # config.py (Pydantic Settings), security, exceptions
├── models/              # SQLAlchemy models (7 tables)
├── schemas/             # Pydantic validation
├── crud/                # Async CRUD layer
├── services/            # Business logic (uses CRUD)
└── db/
    ├── session.py       # Async engine + session factory
    ├── base.py          # Declarative base
    └── seed.py          # Sample data
alembic/                 # Migrations
marine-site/             # Houshou Marine fan frontend
main.py                  # Entry point
```

## Models & relationships

| Model | Relations |
|-------|-----------|
| User | 1:1 Profile, 1:N Posts, 1:N Orders |
| UserProfile | 1:1 User |
| Category | 1:N Products |
| Product | N:1 Category |
| Order | N:1 User, 1:N OrderItems |
| OrderItem | N:1 Order, N:1 Product |
| Post | N:1 User |

## Quick start

```powershell
poetry install
copy .env.example .env
docker compose up -d
poetry run alembic upgrade head
poetry run seed-db
poetry run python main.py
```

- API docs: http://127.0.0.1:8000/docs  
- Marine site: http://127.0.0.1:8000/marine/  
- Health: http://127.0.0.1:8000/api/v1/health  

Use **`poetry run python main.py`** (not bare `python main.py`).

## Alembic

```powershell
poetry run alembic revision --autogenerate -m "describe change"
poetry run alembic upgrade head
```

## Labs

- [docs/LAB4.md](docs/LAB4.md) — PostgreSQL + screenshots for dev branch
