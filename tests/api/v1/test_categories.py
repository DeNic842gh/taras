def test_categories_crud(client) -> None:
    created = client.post(
        "/api/v1/categories",
        json={"name": "Treasure", "description": "Rare goods"},
    )
    assert created.status_code == 201
    category_id = created.json()["id"]

    listed = client.get("/api/v1/categories")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    fetched = client.get(f"/api/v1/categories/{category_id}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Treasure"

    updated = client.put(
        f"/api/v1/categories/{category_id}",
        json={"description": "Updated"},
    )
    assert updated.status_code == 200

    deleted = client.delete(f"/api/v1/categories/{category_id}")
    assert deleted.status_code == 204

    missing = client.get(f"/api/v1/categories/{category_id}")
    assert missing.status_code == 404
