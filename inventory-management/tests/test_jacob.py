# TEST 1: Create a product and validate its fields
def test_product_creation_returns_expected_fields(client):
    response = client.post("/products", json = {"name": "Product", "sku": "A", "unit_price": 1, "quantity_on_hand": 1})
    # Different status codes have different meanings, 201 is the creation code
    assert response.status_code == 201
    product = response.get_json()
    assert product["id"] == 1
    assert product["name"] == "Product"
    assert product["sku"] == "A"
    assert product["unit_price"] == 1
    assert product["quantity_on_hand"] == 1

# TEST 2: Update a product and validate its fields
def test_product_update_returns_expected_fields(client):
    response = client.post("/products", json = {"name": "Product", "sku": "A", "unit_price": 1, "quantity_on_hand": 1})
    assert response.status_code == 201
    response = client.put("/products/1", json = {"name": "Input", "sku": "B", "unit_price": 2, "quantity_on_hand": 2})
    assert response.status_code == 200
    product = response.get_json()
    assert product["id"] == 1
    assert product["name"] == "Input"
    assert product["sku"] == "B"
    assert product["unit_price"] == 2
    assert product["quantity_on_hand"] == 2

# TEST 3: Get quantity on hand of a product and validate its fields
def test_product_quantity_on_hand_retrieval(client):
    response = client.post("/products", json = {"name": "Product", "sku": "A", "unit_price": 1, "quantity_on_hand": 1})
    assert response.status_code == 201
    response = client.get("/products/1/stock-level")
    assert response.status_code == 200
    product = response.get_json()
    assert product["product_id"] == 1
    assert product["quantity_on_hand"] == 1
