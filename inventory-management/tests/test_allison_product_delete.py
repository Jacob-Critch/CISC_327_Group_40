def test_product_delete_nonexistent_product_returns_404(client):
    """Attempting to DELETE a product that does not exist responds with HTTP 404"""

    id_invalid = -1

    response = client.delete(f"/products/{id_invalid}")
    assert response.status_code == 404

def test_product_create_and_then_delete(client):
    """A product POSTed to /products results can be deleted with GET"""

    payload = {
        "name": "Product 1",
        "sku": "AAA",
        "unit_price": 10.00,
        "quantity_on_hand": 10,
        "reorder_level": 5,
    }
    create_resp = client.post("/products", json=payload)
    assert create_resp.status_code == 201
    product_id = create_resp.get_json()["id"]

    product_resp = client.get(f"/products/{product_id}")
    assert product_resp.status_code == 200
    product = product_resp.get_json()

    assert product["name"] == payload["name"]
    assert product["sku"] == payload["sku"]
    assert product["unit_price"] == payload["unit_price"]
    assert product["quantity_on_hand"] == payload["quantity_on_hand"]
    assert product["reorder_level"] == payload["reorder_level"]

    product_resp = client.delete(f"/products/{product_id}")
    assert (product_resp.status_code == 200 or product_resp.status_code == 204)

    product_resp = client.get(f"/products/{product_id}")
    assert product_resp.status_code == 404