def _register(client, username: str, email: str) -> None:
    client.post(
        "/api/v1/auth/register",
        json={"username": username, "email": email, "password": "password99"},
    )


def test_protected_post_crud(client) -> None:
    _register(client, "author", "author@example.com")
    created = client.post(
        "/api/v1/posts",
        json={"title": "Ahoy!", "content": "First log entry"},
    )
    assert created.status_code == 201
    post_id = created.json()["id"]
    assert created.json()["owner_id"] == 1

    mine = client.get("/api/v1/posts/me")
    assert mine.status_code == 200
    assert len(mine.json()) == 1

    updated = client.put(
        f"/api/v1/posts/{post_id}",
        json={"title": "Updated Ahoy!"},
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Updated Ahoy!"

    deleted = client.delete(f"/api/v1/posts/{post_id}")
    assert deleted.status_code == 204


def test_create_post_requires_auth(client) -> None:
    response = client.post(
        "/api/v1/posts",
        json={"title": "Secret", "content": "nope"},
    )
    assert response.status_code == 401


def test_cannot_edit_other_users_post(client) -> None:
    _register(client, "user_a", "a@example.com")
    post = client.post("/api/v1/posts", json={"title": "A post", "content": "x"}).json()

    client.post("/api/v1/auth/logout")
    _register(client, "user_b", "b@example.com")

    forbidden = client.put(
        f"/api/v1/posts/{post['id']}",
        json={"title": "Hijacked"},
    )
    assert forbidden.status_code == 403
