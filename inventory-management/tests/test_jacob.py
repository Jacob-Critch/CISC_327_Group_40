# TEST 1: Create a product and validate its fields
def test_product_creation_returns_expected_fields(client):
    response = client.post("/products", json = {"name": "Product", "quantity_on_hand": 1, "reorder_level": 1, "sku": "A", "unit_price": 1})
    # Different status codes have different meanings, 201 is the creation code
    assert response.status_code == 201
    product = response.get_json()
    assert product["id"] == 1
    assert product["name"] == "Product"
    assert product["quantity_on_hand"] == 1
    assert product["reorder_level"] == 1
    assert product["sku"] == "A"
    assert product["unit_price"] == 1 

# TEST 2: Update a product and validate its fields
def test_product_update_returns_expected_fields(client):
    response = client.post("/products", json = {"name": "Product", "quantity_on_hand": 1, "reorder_level": 1, "sku": "A", "unit_price": 1})
    assert response.status_code == 201
    response = client.put("/products/1", json = {"name": "Input", "quantity_on_hand": 2, "reorder_level": 2, "sku": "B", "unit_price": 2})
    assert response.status_code == 200
    product = response.get_json()
    assert product["id"] == 1
    assert product["name"] == "Input"
    assert product["quantity_on_hand"] == 2
    assert product["reorder_level"] == 2
    assert product["sku"] == "B"
    assert product["unit_price"] == 2

# TEST 3: Get quantity on hand of a product and validate its fields
def test_product_quantity_on_hand_retrieval_returns_expected_fields(client):
    response = client.post("/products", json = {"name": "Product", "sku": "A", "quantity_on_hand": 1})
    assert response.status_code == 201
    response = client.get("/products/1/stock-level")
    assert response.status_code == 200
    product = response.get_json()
    assert product["product_id"] == 1
    assert product["quantity_on_hand"] == 1

# TEST 4: Create a supplier and validate its fields
def test_supplier_creation_returns_expected_fields(client):
    response = client.post("/suppliers", json = {"contact_email": "johndoe@email.com", "name": "Supplier"})
    assert response.status_code == 201
    supplier = response.get_json()
    assert supplier["contact_email"] == "johndoe@email.com"
    assert supplier["id"] == 1
    assert supplier["name"] == "Supplier"

# Test 5: Update a supplier and validate its fields
def test_supplier_update_returns_expected_fields(client):
    response = client.post("/suppliers", json = {"contact_email": "johndoe@email.com", "name": "Supplier"})
    assert response.status_code == 201
    response = client.put("/suppliers/1", json = {"contact_email": "janedoe@email.com", "name": "Buyer"})
    assert response.status_code == 200
    supplier = response.get_json()
    assert supplier["contact_email"] == "janedoe@email.com"
    assert supplier["id"] == 1
    assert supplier["name"] == "Buyer"
