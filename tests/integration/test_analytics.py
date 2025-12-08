

def test_get_popular_products(client):
    response = client.get("/api/v1/analytics/popular-products")
    assert response.status_code == 200
