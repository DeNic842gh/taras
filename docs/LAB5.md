# Lab 5 — JWT authentication, cookies, protected endpoints

## Requirements covered

- **Registration** — `POST /api/v1/auth/register` (username, email, password)
- **Login** — `POST /api/v1/auth/login` (username, password)
- **JWT** — returned in JSON (`access_token`) and stored in an **HttpOnly cookie**
- **Logout** — `POST /api/v1/auth/logout` clears the cookie
- **Passwords** — bcrypt hashes only (`passlib` + `bcrypt`); never stored in plain text
- **Database** — users and posts in PostgreSQL (`USE_MEMORY_STORE=false`)

## Setup

```powershell
# .env: USE_MEMORY_STORE=false, DATABASE_URL with localhost for host runs
poetry install
poetry run alembic upgrade head
poetry run python main.py
```

Docker:

```powershell
docker compose up -d --build
docker exec fastapi_app poetry run alembic upgrade head
```

## Auth endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/auth/register` | — | Create account, JWT + cookie |
| POST | `/api/v1/auth/login` | — | Login, JWT + cookie |
| POST | `/api/v1/auth/logout` | — | Clear cookie |
| GET | `/api/v1/auth/me` | Yes | Current user (Bearer or cookie) |

## Protected endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/users/me` | Own profile |
| PUT | `/api/v1/users/me` | Update own profile |
| GET | `/api/v1/posts/me` | Own posts |
| POST | `/api/v1/posts` | Create post (owner = current user) |
| PUT | `/api/v1/posts/{id}` | Update own post only |
| DELETE | `/api/v1/posts/{id}` | Delete own post only |

Public: `GET /api/v1/posts`, `GET /api/v1/posts/{id}`, user list/CRUD (admin-style).

## Postman / curl

**Register:**

```http
POST http://127.0.0.1:8000/api/v1/auth/register
Content-Type: application/json

{
  "username": "senchou",
  "email": "marine@example.com",
  "password": "ahoy12345"
}
```

**Login** (saves cookie in Postman automatically if enabled):

```http
POST http://127.0.0.1:8000/api/v1/auth/login
Content-Type: application/json

{
  "username": "senchou",
  "password": "ahoy12345"
}
```

**Protected request** — either header:

```http
Authorization: Bearer <access_token>
```

or send the `access_token` cookie from login.

## Tests

```powershell
poetry run pytest tests/api/v1/test_auth.py tests/api/v1/test_posts_auth.py -v
```

## Screenshots for report

1. DBeaver — `users` table showing `hashed_password` (bcrypt `$2b$...`)
2. Postman — register/login response with `access_token`
3. Postman — `GET /api/v1/users/me` with cookie or Bearer
4. Postman — `POST /api/v1/posts` without auth → 401
5. Postman — create post as user A, edit as user B → 403
