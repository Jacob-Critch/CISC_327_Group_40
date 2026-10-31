# TEST 1: Create a product
def test_product_creation_returns_expected_fields(client):
    response = client.post("/products", json = {"id": 1, "name": "Product", "sku": "A", "unit_price": 1, "quantity_on_hand": 1})
    # Different status codes have different meanings, 201 is the creation code
    assert response.status_code == 201
    product = response.get_json()
    assert product["id"] == 1
    assert product["name"] == "Product"
    assert product["sku"] == "A"
    assert product["unit_price"] == 1
    assert product["quantity_on_hand"] == 1
