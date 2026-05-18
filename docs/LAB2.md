# Lab 2 — Docker (2 containers only)

Always **one stack** = **1 API** + **1 PostgreSQL**. Do not run production and development compose at the same time.

| Mode | Command | API URL | Containers |
|------|---------|---------|------------|
| Production | `docker compose up -d --build` | http://127.0.0.1:8080 | `fastapi_app`, `fastapi_postgres` |
| Development | `docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build` | http://127.0.0.1:8000 | same 2 names, with `--reload` + `.:/app` |

`docker-compose.dev.yml` is an **override** — it does not start extra containers.

## Clean up old 4-container setup

```powershell
docker rm -f fastapi_app_prod fastapi_postgres_prod fastapi_app_dev fastapi_postgres_dev
docker compose -p fastapi-prod down
docker compose -p fastapi-dev down
```

## Dev branch files

- `docs/LAB2_COMMANDS.txt` — command list
- `docs/pip_list.txt` — `docker exec fastapi_app pip list`
- `docs/LAB2_SCREENSHOTS/` — your screenshots
