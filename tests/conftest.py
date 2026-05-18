import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage.user_memory import user_memory_store


@pytest.fixture(autouse=True)
def clear_user_store() -> None:
    user_memory_store.reset()
    yield
    user_memory_store.reset()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
