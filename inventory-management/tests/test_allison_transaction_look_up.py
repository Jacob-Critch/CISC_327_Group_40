def test_transaction_look_up_nonexistent_product_id_returns_empty_list(client):
    """Attempting to GET a transaction that does not exist responds with HTTP 404"""

    id_invalid = -1

    response = client.get(f"/transactions?product_id={id_invalid}")
    assert response.status_code == 200
    assert response.get_json() == []

def test_transaction_look_up_nonexistent_supplier_id_returns_empty_list(client):
    """Attempting to GET a transaction that does not exist responds with HTTP 404"""

    id_invalid = -1

    response = client.get(f"/transactions?supplier_id={id_invalid}")
    assert response.status_code == 200
    assert response.get_json() == []

def test_transaction_create_and_look_up_returns(client):
    """A transaction POSTed to /transactions results can be retrieved with GET"""

    from datetime import date

    #
    payload_product = {
        "name": "Product 1",
        "sku": "AAA",
        "unit_price": 10.00,
        "quantity_on_hand": 10,
        "reorder_level": 5,
    }
    create_resp = client.post("/products", json=payload_product)
    assert create_resp.status_code == 201
    product_id = create_resp.get_json()["id"]

    product_resp = client.get(f"/products/{product_id}")
    assert product_resp.status_code == 200
    product = product_resp.get_json()

    assert product["name"] == payload_product["name"]
    assert product["sku"] == payload_product["sku"]
    assert product["unit_price"] == payload_product["unit_price"]
    assert product["quantity_on_hand"] == payload_product["quantity_on_hand"]
    assert product["reorder_level"] == payload_product["reorder_level"]

    payload_supplier = {
        "name": "Supplier 1",
        "contact_email": "test@test.test",
    }
    create_resp = client.post("/suppliers", json=payload_supplier)
    assert create_resp.status_code == 201
    supplier_id = create_resp.get_json()["id"]

    supplier_resp = client.get(f"/suppliers/{supplier_id}")
    assert supplier_resp.status_code == 200
    supplier = supplier_resp.get_json()

    assert supplier["name"] == payload_supplier["name"]
    assert supplier["contact_email"] == payload_supplier["contact_email"]

    payload = {
        "product_id": product_id,
        "supplier_id": supplier_id,
        "type": "IN",
        "quantity": 10,
        "transaction_date": date.today().isoformat(),
    }
    create_resp = client.post("/transactions", json=payload)
    assert create_resp.status_code == 201
    transaction_id = create_resp.get_json()["id"]

    transaction_resp = client.get(f"/transactions?product_id={product_id}&supplier_id={supplier_id}")
    assert transaction_resp.status_code == 200
    transactions = transaction_resp.get_json()

    for transaction in transactions:
        if transaction["id"] == transaction_id:
            assert transaction["product_id"] == payload["product_id"]
            assert transaction["supplier_id"] == payload["supplier_id"]
            assert transaction["type"] == payload["type"]
            assert transaction["quantity"] == payload["quantity"]
            assert transaction["transaction_date"] == payload["transaction_date"]