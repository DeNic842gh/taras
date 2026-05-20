# Lab 4 — PostgreSQL + Alembic

## Models (7 tables)

| Model | Relationships |
|-------|----------------|
| **User** | 1:1 `UserProfile`, 1:N `Post`, 1:N `Order` |
| **UserProfile** | 1:1 `User` |
| **Category** | 1:N `Product` |
| **Product** | N:1 `Category`, referenced by `OrderItem` |
| **Post** | N:1 `User` |
| **Order** | N:1 `User`, 1:N `OrderItem` |
| **OrderItem** | N:1 `Order`, N:1 `Product` |

## Setup

```powershell
cd c:\Users\Denis\Desktop\taras
copy .env.example .env
docker compose up -d
poetry install
poetry run alembic upgrade head
poetry run seed-db
poetry run serve
```

Health: http://127.0.0.1:8000/api/v1/health → `"database": "connected"`

## API endpoints (all async CRUD)

| Resource | Prefix |
|----------|--------|
| Users | `/api/v1/users` |
| Profiles | `/api/v1/profiles` |
| Categories | `/api/v1/categories` |
| Products | `/api/v1/products` |
| Posts | `/api/v1/posts` |
| Orders | `/api/v1/orders` |
| Order items | `/api/v1/order-items` |

## Dev branch screenshots

Save under `docs/LAB4_SCREENSHOTS/`:

1. **tables** — pgAdmin or DBeaver: list all 7 tables
2. **fields** — column list for `users`, `products`, `orders` (or all tables)
3. **data** — `SELECT *` from each table after `poetry run seed-db`

### psql quick checks

```powershell
docker exec -it fastapi_postgres psql -U app -d fastapi_db -c "\dt"
docker exec -it fastapi_postgres psql -U app -d fastapi_db -c "\d users"
docker exec -it fastapi_postgres psql -U app -d fastapi_db -c "SELECT * FROM users;"
docker exec -it fastapi_postgres psql -U app -d fastapi_db -c "SELECT * FROM categories;"
docker exec -it fastapi_postgres psql -U app -d fastapi_db -c "SELECT * FROM products;"
```

## Configuration

- **Pydantic Settings:** `app/core/config.py`
- **Session factory:** `app/db/session.py` → `AsyncSessionLocal`, `get_db()`
- **Migrations:** `alembic/versions/20260519_0001_initial_schema.py`
- **Seed data:** `app/db/seed.py` (`poetry run seed-db`)
