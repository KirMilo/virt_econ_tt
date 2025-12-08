def test_post_purchase_product(client):
    response = client.post(
        "/api/v1/products/{product_id}/purchase".format(product_id=1),
        json={"user_id": 1},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


# def test_post_purchase_product_for_non_existent_product(client):
#     non_existent_product_id = 1000000
#     response = client.post(
#         "/api/v1/products/{product_id}/purchase".format(product_id=non_existent_product_id),
#         json={"user_id": 1},
#     )
#     assert response.status_code == 404
#     assert response.json()["detail"] == f"Product {non_existent_product_id} not found"


def test_post_purchase_product_for_non_existent_user(client):
    non_existent_user_id = 1000000
    response = client.post(
        "/api/v1/products/{product_id}/purchase".format(product_id=1),
        json={"user_id": non_existent_user_id},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == f"User {non_existent_user_id} not found"

#
# def test_post_use_product(client):
#     product_id = 1
#     response = client.post(
#         "/api/v1/products/{product_id}/use".format(product_id=product_id),
#         json={"user_id": 1},
#     )
#     assert response.status_code == 200
#     assert response.json() == {"product_id": product_id, "quantity": 0}
