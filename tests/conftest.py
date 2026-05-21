import os

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

from app.db.base import Base
from app.db.session import get_db
from app.main import app

test_engine = create_async_engine(os.environ["DATABASE_URL"], echo=False)
TestSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(autouse=True)
async def prepare_database() -> None:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def _override_get_db():
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
