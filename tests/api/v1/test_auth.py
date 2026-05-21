def test_register_login_cookie_and_me(client) -> None:
    register_payload = {
        "username": "senchou",
        "email": "marine@houshou.pirate",
        "password": "ahoy12345",
        "full_name": "Houshou Marine",
    }
    registered = client.post("/api/v1/auth/register", json=register_payload)
    assert registered.status_code == 201
    body = registered.json()
    assert body["token_type"] == "bearer"
    assert body["user"]["username"] == "senchou"
    assert "access_token" in client.cookies

    me_cookie = client.get("/api/v1/auth/me")
    assert me_cookie.status_code == 200
    assert me_cookie.json()["email"] == "marine@houshou.pirate"

    client.cookies.clear()
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "senchou", "password": "ahoy12345"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    me_bearer = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_bearer.status_code == 200
    assert me_bearer.json()["username"] == "senchou"


def test_login_invalid_credentials(client) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "nobody", "password": "wrongpass1"},
    )
    assert response.status_code == 401


def test_logout_clears_cookie(client) -> None:
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "crew",
            "email": "crew@example.com",
            "password": "password99",
        },
    )
    assert client.cookies.get("access_token")
    logout = client.post("/api/v1/auth/logout")
    assert logout.status_code == 204
