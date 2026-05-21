def test_register_and_login(client) -> None:
    register_payload = {
        "username": "pirate_crew",
        "email": "pirate@example.com",
        "password": "secret123",
    }
    registered = client.post("/api/v1/auth/register", json=register_payload)
    assert registered.status_code == 201
    body = registered.json()
    assert body["token_type"] == "bearer"
    assert body["user"]["username"] == "pirate_crew"
    token = body["access_token"]

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "pirate@example.com", "password": "secret123"},
    )
    assert login.status_code == 200
    assert login.json()["access_token"]

    me = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me.status_code == 200
    assert me.json()["email"] == "pirate@example.com"
