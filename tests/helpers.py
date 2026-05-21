from decimal import Decimal

from fastapi.testclient import TestClient

from app.schemas.category import CategoryCreate
from app.schemas.order import OrderCreate
from app.schemas.order_item import OrderItemCreate
from app.schemas.post import PostCreate
from app.schemas.product import ProductCreate
from app.schemas.user import UserCreate
from app.schemas.user_profile import UserProfileCreate


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def register_user(
    client: TestClient,
    *,
    username: str = "testuser",
    email: str = "test@example.com",
    password: str = "password99",
) -> tuple[str, dict]:
    response = client.post(
        "/api/v1/auth/register",
        json={"username": username, "email": email, "password": password},
    )
    assert response.status_code == 201, response.text
    body = response.json()
    return body["access_token"], body["user"]


def login_user(
    client: TestClient,
    *,
    email: str = "test@example.com",
    password: str = "password99",
) -> tuple[str, dict]:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    return body["access_token"], body["user"]


def user_create_schema(
    *,
    username: str = "dbuser",
    email: str = "dbuser@example.com",
    password: str = "password99",
) -> UserCreate:
    return UserCreate(
        username=username,
        email=email,
        password=password,
        full_name="Test User",
        is_active=True,
    )


def category_create_schema(*, name: str = "Merch") -> CategoryCreate:
    return CategoryCreate(name=name, description="Test category")


def product_create_schema(*, category_id: int, name: str = "Hat") -> ProductCreate:
    return ProductCreate(
        name=name,
        description="Test product",
        price=Decimal("19.99"),
        stock=10,
        category_id=category_id,
    )


def post_create_schema(*, title: str = "Ahoy") -> PostCreate:
    return PostCreate(title=title, content="Test post body")


def profile_create_schema(*, user_id: int) -> UserProfileCreate:
    return UserProfileCreate(user_id=user_id, bio="Test bio", country="JP")


def order_create_schema(*, user_id: int) -> OrderCreate:
    return OrderCreate(user_id=user_id, status="pending")


def order_item_create_schema(*, order_id: int, product_id: int) -> OrderItemCreate:
    return OrderItemCreate(
        order_id=order_id,
        product_id=product_id,
        quantity=2,
        unit_price=Decimal("9.99"),
    )
