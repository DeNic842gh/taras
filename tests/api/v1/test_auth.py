from tests.helpers import auth_header, register_user


def test_register_and_login(client) -> None:
    token, user = register_user(
        client,
        username="pirate_crew",
        email="pirate@example.com",
    )
    assert user["username"] == "pirate_crew"

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "pirate@example.com", "password": "password99"},
    )
    assert login.status_code == 200
    assert login.json()["access_token"]

    me = client.get("/api/v1/auth/me", headers=auth_header(token))
    assert me.status_code == 200
    assert me.json()["email"] == "pirate@example.com"


def test_register_duplicate_email(client) -> None:
    register_user(client, username="user1", email="dup@example.com")
    second = client.post(
        "/api/v1/auth/register",
        json={"username": "user2", "email": "dup@example.com", "password": "password99"},
    )
    assert second.status_code == 409


def test_login_invalid_credentials(client) -> None:
    register_user(client, email="valid@example.com")
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "valid@example.com", "password": "wrongpass9"},
    )
    assert response.status_code == 401


def test_auth_me_requires_token(client) -> None:
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
