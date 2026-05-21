from tests.helpers import register_user


def test_posts_crud(client) -> None:
    _, user = register_user(client, username="poster", email="poster@example.com")
    owner_id = user["id"]

    created = client.post(
        "/api/v1/posts",
        params={"owner_id": owner_id},
        json={"title": "Captain log", "content": "Ahoy"},
    )
    assert created.status_code == 201
    post_id = created.json()["id"]

    listed = client.get("/api/v1/posts")
    assert listed.status_code == 200
    assert any(p["id"] == post_id for p in listed.json())

    fetched = client.get(f"/api/v1/posts/{post_id}")
    assert fetched.status_code == 200

    updated = client.put(
        f"/api/v1/posts/{post_id}",
        json={"title": "Updated log"},
    )
    assert updated.status_code == 200

    deleted = client.delete(f"/api/v1/posts/{post_id}")
    assert deleted.status_code == 204

    assert client.get(f"/api/v1/posts/{post_id}").status_code == 404


def test_post_not_found(client) -> None:
    assert client.get("/api/v1/posts/99999").status_code == 404
