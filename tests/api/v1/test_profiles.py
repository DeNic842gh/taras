from tests.helpers import register_user


def test_profiles_crud(client) -> None:
    _, user = register_user(client, username="profileuser", email="profile@example.com")
    user_id = user["id"]

    created = client.post(
        "/api/v1/profiles",
        json={"user_id": user_id, "bio": "Ahoy!", "country": "Japan"},
    )
    assert created.status_code == 201
    profile_id = created.json()["id"]

    by_user = client.get(f"/api/v1/profiles/by-user/{user_id}")
    assert by_user.status_code == 200
    assert by_user.json()["bio"] == "Ahoy!"

    fetched = client.get(f"/api/v1/profiles/{profile_id}")
    assert fetched.status_code == 200

    listed = client.get("/api/v1/profiles")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    updated = client.put(
        f"/api/v1/profiles/{profile_id}",
        json={"bio": "Updated bio"},
    )
    assert updated.status_code == 200

    duplicate = client.post(
        "/api/v1/profiles",
        json={"user_id": user_id, "bio": "Again"},
    )
    assert duplicate.status_code == 409

    deleted = client.delete(f"/api/v1/profiles/{profile_id}")
    assert deleted.status_code == 204

    assert client.get(f"/api/v1/profiles/{profile_id}").status_code == 404
