from tests.helpers import register_user


def _create_order_with_product(client) -> tuple[int, int, int]:
    _, user = register_user(
        client,
        username=f"shopper_{id(client)}",
        email=f"shopper_{id(client)}@example.com",
    )
    category = client.post(
        "/api/v1/categories",
        json={"name": f"Cat_{id(client)}", "description": "x"},
    ).json()
    product = client.post(
        "/api/v1/products",
        json={
            "name": "Item",
            "price": "5.00",
            "stock": 1,
            "category_id": category["id"],
        },
    ).json()
    order = client.post(
        "/api/v1/orders",
        json={"user_id": user["id"], "status": "pending"},
    ).json()
    return order["id"], product["id"], user["id"]


def test_order_items_crud(client) -> None:
    order_id, product_id, _ = _create_order_with_product(client)

    created = client.post(
        "/api/v1/order-items",
        json={
            "order_id": order_id,
            "product_id": product_id,
            "quantity": 1,
            "unit_price": "5.00",
        },
    )
    assert created.status_code == 201
    item_id = created.json()["id"]

    listed = client.get("/api/v1/order-items")
    assert listed.status_code == 200

    fetched = client.get(f"/api/v1/order-items/{item_id}")
    assert fetched.status_code == 200

    updated = client.put(
        f"/api/v1/order-items/{item_id}",
        json={"quantity": 2},
    )
    assert updated.status_code == 200
    assert updated.json()["quantity"] == 2

    deleted = client.delete(f"/api/v1/order-items/{item_id}")
    assert deleted.status_code == 204

    assert client.get(f"/api/v1/order-items/{item_id}").status_code == 404
