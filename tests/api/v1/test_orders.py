from tests.helpers import register_user


def test_orders_crud(client) -> None:
    _, user = register_user(client, username="buyer", email="buyer@example.com")
    user_id = user["id"]

    created = client.post(
        "/api/v1/orders",
        json={"user_id": user_id, "status": "pending"},
    )
    assert created.status_code == 201
    order_id = created.json()["id"]

    listed = client.get("/api/v1/orders")
    assert listed.status_code == 200

    fetched = client.get(f"/api/v1/orders/{order_id}")
    assert fetched.status_code == 200

    updated = client.put(
        f"/api/v1/orders/{order_id}",
        json={"status": "paid", "total_amount": "42.50"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "paid"

    deleted = client.delete(f"/api/v1/orders/{order_id}")
    assert deleted.status_code == 204

    assert client.get(f"/api/v1/orders/{order_id}").status_code == 404
