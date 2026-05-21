def test_products_crud(client) -> None:
    category = client.post(
        "/api/v1/categories",
        json={"name": "Apparel", "description": "Clothes"},
    ).json()

    created = client.post(
        "/api/v1/products",
        json={
            "name": "Captain Hat",
            "description": "Red hat",
            "price": "29.99",
            "stock": 5,
            "category_id": category["id"],
        },
    )
    assert created.status_code == 201
    product_id = created.json()["id"]

    listed = client.get("/api/v1/products")
    assert listed.status_code == 200
    assert len(listed.json()) >= 1

    fetched = client.get(f"/api/v1/products/{product_id}")
    assert fetched.status_code == 200

    updated = client.put(
        f"/api/v1/products/{product_id}",
        json={"stock": 10},
    )
    assert updated.status_code == 200
    assert updated.json()["stock"] == 10

    deleted = client.delete(f"/api/v1/products/{product_id}")
    assert deleted.status_code == 204

    assert client.get(f"/api/v1/products/{product_id}").status_code == 404
