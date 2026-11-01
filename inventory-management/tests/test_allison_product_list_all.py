def test_list_products_returns_empty_list_initially(client):
    """Products endpoint returns an empty list when no products have been added.

    This is the simplest possible test — it confirms the endpoint exists,
    responds with HTTP 200, and that the store starts clean for every test
    (thanks to the reset() call in conftest.py).

    NOTE: THIS IS FROM THE ORIGINAL test_examples.py
    """
    response = client.get("/products")
    assert response.status_code == 200
    assert response.get_json() == []

def test_product_create_products_then_list_all(client):
    """All product POSTed to /products can be retrieved as an array with GET"""

    # Define products to be POSTed
    product_1 = {
        "name": "Product 1",
        "sku": "AAA",
        "unit_price": 10.00,
        "quantity_on_hand": 10,
        "reorder_level": 5,
    }
    product_2 = {
        "name": "Product 2",
        "sku": "BBB",
        "unit_price": 20.00,
        "quantity_on_hand": 20,
        "reorder_level": 10,
    }
    payload = [product_1, product_2]

    # POST products
    create_resp = []
    product_id = []
    for i in len(payload):
        create_resp.append(client.post("/products", json=payload[i]))
        assert create_resp[i].status_code == 201
        product_id.append(create_resp[i].get_json()["id"])

    # Get all products in /products with GET
    product_resp = client.get("/products")

    # Ensure GET has worked
    assert product_resp.status_code == 200
    products = product_resp.get_json()
    assert len(products) == len(payload)

    # Ensure the product was retrieved correctly
    for i in range(len(products)):
        assert products[i]["name"] == payload[i]["name"]
        assert products[i]["sku"] == payload[i]["sku"]
        assert products[i]["unit_price"] == payload[i]["unit_price"]
        assert products[i]["quantity_on_hand"] == payload[i]["quantity_on_hand"]
        assert products[i]["reorder_level"] == payload[i]["reorder_level"]