
def test_post_add_funds(client):
    amount = 10
    response = client.post(
        "/api/v1/users/{user_id}/add-funds".format(user_id=1),
        json={"amount": amount},
        headers={
            "Idempotency-Key": client.get("/api/v1/idempotency/generate-key/").json().get("idempotency_key")
        }
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Payment successfully processed."
    assert response.json()["amount"] == amount


def test_get_inventory(client):
    response = client.get("/api/v1/users/{user_id}/inventory".format(user_id=1))
    assert response.status_code == 200
