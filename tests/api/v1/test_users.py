def test_users_crud_flow(client) -> None:
    # POST — create
    create_payload = {
        "email": "alice@example.com",
        "full_name": "Alice",
        "password": "secret123",
        "is_active": True,
    }
    created = client.post("/api/v1/users", json=create_payload)
    assert created.status_code == 201
    user = created.json()
    assert user["email"] == "alice@example.com"
    user_id = user["id"]

    # GET — list
    listed = client.get("/api/v1/users")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    # GET — by id
    fetched = client.get(f"/api/v1/users/{user_id}")
    assert fetched.status_code == 200
    assert fetched.json()["full_name"] == "Alice"

    # PUT — update
    updated = client.put(
        f"/api/v1/users/{user_id}",
        json={"full_name": "Alice Updated", "is_active": False},
    )
    assert updated.status_code == 200
    assert updated.json()["full_name"] == "Alice Updated"
    assert updated.json()["is_active"] is False

    # DELETE
    deleted = client.delete(f"/api/v1/users/{user_id}")
    assert deleted.status_code == 204

    # GET — not found after delete
    missing = client.get(f"/api/v1/users/{user_id}")
    assert missing.status_code == 404


def test_create_user_validation_error(client) -> None:
    response = client.post(
        "/api/v1/users",
        json={"email": "bad-email", "password": "short"},
    )
    assert response.status_code == 422
