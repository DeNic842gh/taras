# Lab 3 — Users CRUD (in-memory dict)

## Features

- **GET** `/api/v1/users` — list users
- **GET** `/api/v1/users/{id}` — get one user
- **POST** `/api/v1/users` — create user (Pydantic validation)
- **PUT** `/api/v1/users/{id}` — update user
- **DELETE** `/api/v1/users/{id}` — delete user (204)

Storage: `app/storage/user_memory.py` (Python `dict`, thread-safe).

## Entry point

```powershell
python main.py
```

Docker runs the same: `CMD ["python", "main.py"]`.

## Run locally

```powershell
poetry install
copy .env.example .env
python main.py
```

Swagger: http://127.0.0.1:8000/docs

## Postman (dev branch screenshot)

1. Import `docs/postman/Lab3_Users_CRUD.postman_collection.json`
2. Set variable `base_url` = `http://127.0.0.1:8000`
3. Run requests in order: **POST** → **GET list** → **GET by id** → **PUT** → **DELETE**
4. After **POST**, copy `id` from response into variable `user_id`
5. Save screenshot to `docs/LAB3_SCREENSHOTS/postman_crud.png`

## Dev branch deliverable

Commit on `dev`:

- Lab 3 code
- `docs/postman/Lab3_Users_CRUD.postman_collection.json`
- `docs/LAB3_SCREENSHOTS/postman_crud.png` (your screenshot)
