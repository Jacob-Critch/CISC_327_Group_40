def test_transaction_look_up_nonexistent_product_id_returns_404(client):
    """Attempting to GET a transaction that does not exist responds with HTTP 404"""

    id_invalid = -1

    response = client.get(f"/transactions?product_id={id_invalid}")
    assert response.status_code == 404

def test_transaction_look_up_nonexistent_supplier_id_returns_404(client):
    """Attempting to GET a transaction that does not exist responds with HTTP 404"""

    id_invalid = -1

    response = client.get(f"/transactions?supplier_id={id_invalid}")
    assert response.status_code == 404

def test_transaction_create_and_look_up_returns(client):
    """A transaction POSTed to /transaction results can be retrieved with GET"""

    import date

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
    #

    #
    #

    payload = {
        "product_id": product_id,
        "supplier_id": supplier_id,
        "type": "IN",
        "quantity": 10,
        "transaction_date": date.today(),
    }
    create_resp = client.post("/transaction", json=payload)
    assert create_resp.status_code == 201
    transaction_id = create_resp.get_json()["id"]

    transaction_resp = client.get(f"/transaction/{transaction_id}")
    assert transaction_resp.status_code == 200
    transaction = transaction_resp.get_json()

    assert transaction["product_id"] == payload["product_id"]
    assert transaction["supplier_id"] == payload["supplier_id"]
    assert transaction["type"] == payload["type"]
    assert transaction["quantity"] == payload["quantity"]
    assert transaction["transaction_date"] == payload["transaction_date"]