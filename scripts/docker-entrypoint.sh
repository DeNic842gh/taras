#!/bin/sh
set -e

host="${POSTGRES_HOST:-db}"
port="${POSTGRES_PORT:-5432}"
user="${POSTGRES_USER:-app}"
db="${POSTGRES_DB:-fastapi_db}"

echo "Waiting for PostgreSQL at ${host}:${port}..."
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30; do
  if pg_isready -h "$host" -p "$port" -U "$user" -d "$db" >/dev/null 2>&1; then
    echo "PostgreSQL is ready."
    break
  fi
  echo "  attempt $i/30 — sleeping 3s"
  sleep 3
done

echo "Running Alembic migrations..."
poetry run alembic upgrade head

echo "Starting FastAPI..."
exec python main.py
