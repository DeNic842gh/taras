# Lab 6 — Full test coverage with separate PostgreSQL

## Requirements

- Tests for **every API endpoint**
- Tests for **every CRUD / DB interaction** (`app/crud/*`)
- **Dependency override** for `get_db` during tests
- **Separate PostgreSQL database** — not the production `fastapi_db`

| | Production | Tests |
|---|------------|--------|
| Container | `fastapi_postgres` | `fastapi_postgres_test` |
| Port (host) | `5432` | `5433` |
| Database | `fastapi_db` | `fastapi_test_db` |

## Setup

```powershell
# 1. Start test database only
docker compose -f docker-compose.test.yml up -d

# 2. Optional: copy test DB settings to .env
# TEST_DATABASE_URL=postgresql+asyncpg://app:appsecret@127.0.0.1:5433/fastapi_test_db

# 3. Run all tests
poetry run pytest -v
```

Production stack (`docker compose up`) is **not** required for tests, only the test DB container.

## How it works

`tests/conftest.py`:

1. Connects to `TEST_DATABASE_URL` (port **5433**, db **fastapi_test_db**)
2. Overrides `get_db` → sessions use the test engine
3. Overrides `check_database_connection` → health checks hit the test DB
4. Before each test: `drop_all` + `create_all` on the **test** database only

## Test layout

```
tests/
├── conftest.py          # test DB + dependency overrides
├── helpers.py           # factories / auth helpers
├── crud/                # direct CRUD tests (async)
│   ├── test_crud_user.py
│   ├── test_crud_user_profile.py
│   ├── test_crud_category.py
│   ├── test_crud_product.py
│   ├── test_crud_post.py
│   ├── test_crud_order.py
│   └── test_crud_order_item.py
└── api/v1/              # HTTP endpoint tests
    ├── test_health.py
    ├── test_auth.py
    ├── test_users.py
    ├── test_categories.py
    ├── test_products.py
    ├── test_profiles.py
    ├── test_posts.py
    ├── test_orders.py
    └── test_order_items.py
```

## Report screenshots

1. `docker ps` — `fastapi_postgres` and `fastapi_postgres_test` both running
2. DBeaver — two databases on different ports
3. `poetry run pytest -v` — all tests green
