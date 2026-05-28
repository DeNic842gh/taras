#!/bin/sh

host="${POSTGRES_HOST:-db}"
port="${POSTGRES_PORT:-5432}"
user="${POSTGRES_USER:-app}"
db="${POSTGRES_DB:-fastapi_db}"

echo "Waiting for PostgreSQL at ${host}:${port}..."
i=0
while [ "$i" -lt 30 ]; do
  if pg_isready -h "$host" -p "$port" -U "$user" -d "$db" >/dev/null 2>&1; then
    echo "PostgreSQL is ready."
    break
  fi
  i=$((i + 1))
  echo "  attempt ${i}/30 — sleeping 3s"
  sleep 3
done

python -m pip install --no-cache-dir --upgrade --force-reinstall "anyio==4.13.0" >/dev/null 2>&1 || true

echo "Running Alembic migrations..."
poetry run alembic upgrade head

echo "Starting FastAPI (marine site at /marine/)..."
exec python main.py
