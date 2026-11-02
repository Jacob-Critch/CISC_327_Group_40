# TEST 1: Create a product and verify its fields
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

# TEST 2: Update a product and verify its fields
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

# TEST 3: Get quantity on hand of a product and verify its fields
def test_product_quantity_on_hand_retrieval_returns_expected_fields(client):
    response = client.post("/products", json = {"name": "Product", "sku": "A", "quantity_on_hand": 1})
    assert response.status_code == 201
    response = client.get("/products/1/stock-level")
    assert response.status_code == 200
    product = response.get_json()
    assert product["product_id"] == 1
    assert product["quantity_on_hand"] == 1

# TEST 4: Create a supplier and verify its fields
def test_supplier_creation_returns_expected_fields(client):
    response = client.post("/suppliers", json = {"contact_email": "johndoe@email.com", "name": "Supplier"})
    assert response.status_code == 201
    supplier = response.get_json()
    assert supplier["contact_email"] == "johndoe@email.com"
    assert supplier["id"] == 1
    assert supplier["name"] == "Supplier"

# Test 5: Update a supplier and verify its fields
def test_supplier_update_returns_expected_fields(client):
    response = client.post("/suppliers", json = {"contact_email": "johndoe@email.com", "name": "Supplier"})
    assert response.status_code == 201
    response = client.put("/suppliers/1", json = {"contact_email": "janedoe@email.com", "name": "Buyer"})
    assert response.status_code == 200
    supplier = response.get_json()
    assert supplier["contact_email"] == "janedoe@email.com"
    assert supplier["id"] == 1
    assert supplier["name"] == "Buyer"

# Test 6: Record a stock movement and verify its fields
def test_stock_movement_recording_returns_expected_fields(client):
    response = client.post("/products", json = {"name": "Stock Movement", "quantity_on_hand": 1, "reorder_level": 1, "sku": "A", "unit_price": 1})
    assert response.status_code == 201
    stockMovement = response.get_json()
    assert stockMovement["name"] == "Stock Movement"
    assert stockMovement["quantity_on_hand"] == 1
    assert stockMovement["reorder_level"] == 1
    assert stockMovement["sku"] == "A"
    assert stockMovement["unit_price"] == 1

# Functional enhancement beginning
# Test 7: Invoke stock alerts on a threshold product and verify its fields
def test_stock_alerts_threshold_invocation_returns_expected_fields(client):
    # Create a threshold product and validate its fields
    response = client.post("/products", json = {"name": "Product", "quantity_on_hand": 1, "reorder_level": 2, "sku": "A", "unit_price": 1})
    assert response.status_code == 201
    product = response.get_json()
    assert product["id"] == 1
    assert product["is_below_reorder_level"] == False
    assert product["name"] == "Product"
    assert product["quantity_on_hand"] == 1
    assert product["reorder_level"] == 2
    assert product["sku"] == "A"
    assert product["unit_price"] == 1

    # Invoke the first stock alert and verify its field
    response = client.post("/products/1/is-below-reorder-level")
    assert response.status_code == 200
    stock_alert = response.get_json()
    assert stock_alert["message"] == "Stock alert for Product (1): 1 more are needed to restore target levels."

    # Get the product and verify its fields after the first stock alert invocation
    response = client.get("/products/1")
    assert response.status_code == 200
    product = response.get_json()
    assert product["is_below_reorder_level"] == True

    # Invoke the second stock alert and verify its field
    response = client.post("/products/1/is-below-reorder-level")
    assert response.status_code == 200
    stock_alert = response.get_json()
    assert stock_alert["message"] == "No stock alert for Product (1)."

    # Get the product and verify its fields after the second stock alert invocation
    response = client.get("/products/1")
    assert response.status_code == 200
    product = response.get_json()
    assert product["is_below_reorder_level"] == True    

# Test 8: Invoke a stock alert on non-threshold product and verify its fields
def test_stock_alert_nonthreshold_invocation_returns_expected_fields(client):
    # Create a nonthreshold product and validate its fields
    response = client.post("/products", json = {"name": "Product", "quantity_on_hand": 2, "reorder_level": 2, "sku": "A", "unit_price": 1})
    assert response.status_code == 201
    product = response.get_json()
    assert product["id"] == 1
    assert product["is_below_reorder_level"] == False
    assert product["name"] == "Product"
    assert product["quantity_on_hand"] == 2
    assert product["reorder_level"] == 2
    assert product["sku"] == "A"
    assert product["unit_price"] == 1

    # Invoke a stock alert and verify its field
    response = client.post("/products/1/is-below-reorder-level")
    assert response.status_code == 200
    stock_alert = response.get_json() 
    assert stock_alert["message"] == "No stock alert for Product (1)."

    # Get the product and verify its fields after the stock alert invocation
    response = client.get("/products/1")
    assert response.status_code == 200
    product = response.get_json()
    assert product["is_below_reorder_level"] == False

# Test 9: Invoke stock alerts on a product before and after restock and validate its fields
def test_stock_alerts_incovations_before_and_after_restock_returns_expected_fields(client):
    # Create a threshold product and validate its fields
    response = client.post("/products", json = {"name": "Product", "quantity_on_hand": 1, "reorder_level": 2, "sku": "A", "unit_price": 1})
    assert response.status_code == 201
    product = response.get_json()
    assert product["id"] == 1
    assert product["is_below_reorder_level"] == False
    assert product["name"] == "Product"
    assert product["quantity_on_hand"] == 1
    assert product["reorder_level"] == 2
    assert product["sku"] == "A"
    assert product["unit_price"] == 1

    # Invoke the first stock alert and verify its field
    response = client.post("/products/1/is-below-reorder-level")
    assert response.status_code == 200
    stock_alert = response.get_json()
    assert stock_alert["message"] == "Stock alert for Product (1): 1 more are needed to restore target levels."

    # Get the product and verify its fields after the first stock alert invocation
    response = client.get("/products/1")
    assert response.status_code == 200
    product = response.get_json()
    assert product["is_below_reorder_level"] == True

    # Update the product and verify its fields
    response = client.put("/products/1", json = {"name": "Input", "quantity_on_hand": 2, "reorder_level": 2, "sku": "B", "unit_price": 2})
    assert response.status_code == 200
    product = response.get_json()
    assert product["id"] == 1
    assert product["is_below_reorder_level"] == True
    assert product["name"] == "Input"
    assert product["quantity_on_hand"] == 2
    assert product["reorder_level"] == 2
    assert product["sku"] == "B"
    assert product["unit_price"] == 2
    stock_alert = response.get_json()

    # Invoke the second stock alert and verify its field
    response = client.post("/products/1/is-below-reorder-level")
    assert response.status_code == 200
    stock_alert = response.get_json()
    assert stock_alert["message"] == "No stock alert for Input (1)."

    # Get the product and verify its fields after the second stock alert invocation
    response = client.get("/products/1")
    assert response.status_code == 200
    product = response.get_json()
    assert product["is_below_reorder_level"] == False

# Test 10: Invoke a stock alert on a non-existent product and validate error
def test_stock_alert_invocation_on_nonexistent_product_returns_expected_field(client):
    # Verify error
    response = client.post("/products/1/is-below-reorder-level")
    assert response.status_code == 404
    product = response.get_json()
    assert product["error"] == "Product not found"
# Functional enhancement end
