"""
Lab 6 — tests run against a separate PostgreSQL database with dependency overrides.

Start test DB: docker compose -f docker-compose.test.yml up -d
Run tests:     poetry run pytest
"""

from __future__ import annotations

import asyncio
import os

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

# Must set test DB URL before importing app (production engine uses DATABASE_URL).
os.environ.setdefault(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://app:appsecret@127.0.0.1:5433/fastapi_test_db",
)

from app.core.config import settings
from app.db import session as db_session
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import Category, Product, User

TEST_DATABASE_URL = settings.resolved_test_database_url

test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool, echo=False)
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


def _check_test_database_sync() -> None:
    async def _ping() -> None:
        async with test_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

    try:
        asyncio.run(_ping())
    except Exception as exc:
        pytest.skip(
            f"Test PostgreSQL unavailable at {TEST_DATABASE_URL}. "
            f"Start it with: docker compose -f docker-compose.test.yml up -d\n"
            f"Error: {exc}"
        )


_check_test_database_sync()


async def _override_get_db():
    async with TestSessionLocal() as session:
        yield session


async def _override_check_database_connection() -> bool:
    try:
        async with test_engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


app.dependency_overrides[get_db] = _override_get_db
db_session.check_database_connection = _override_check_database_connection


@pytest_asyncio.fixture(autouse=True)
async def reset_test_database() -> None:
    """Isolate each test with a fresh schema on the test database only."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def auth_token(client: TestClient) -> str:
    from tests.helpers import register_user

    token, _ = register_user(client)
    return token


@pytest.fixture
def auth_headers(auth_token: str) -> dict[str, str]:
    from tests.helpers import auth_header

    return auth_header(auth_token)


@pytest_asyncio.fixture
async def sample_user(db_session: AsyncSession) -> User:
    from app import crud
    from tests.helpers import user_create_schema

    return await crud.user.create(db_session, obj_in=user_create_schema())


@pytest_asyncio.fixture
async def sample_category(db_session: AsyncSession) -> Category:
    from app import crud
    from tests.helpers import category_create_schema

    return await crud.category.create(db_session, obj_in=category_create_schema())


@pytest_asyncio.fixture
async def sample_product(db_session: AsyncSession, sample_category: Category) -> Product:
    from app import crud
    from tests.helpers import product_create_schema

    return await crud.product.create(
        db_session,
        obj_in=product_create_schema(category_id=sample_category.id),
    )
