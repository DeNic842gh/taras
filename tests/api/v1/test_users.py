def test_users_route_registered(client) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "/api/v1/users" in response.json()["paths"]
