def test_list_suppliers_returns_empty_list_initially(client):
    """Suppliers endpoint returns an empty list when no suppliers have been added."""
    response = client.get("/suppliers")
    assert response.status_code == 200
    assert response.get_json() == []

def test_supplier_create_suppliers_then_list_all(client):
    """All supplier POSTed to /suppliers can be retrieved as an array with GET"""

    # Define suppliers to be POSTed
    supplier_1 = {
        "name": "Supplier 1",
        "contact_email": "test@test.test",
    }
    supplier_2 = {
        "name": "supplier 2",
        "contact_email": "test2@test.test",
    }
    payload = [supplier_1, supplier_2]

    # POST suppliers
    create_resp = []
    supplier_id = []
    for i in range(len(payload)):
        create_resp.append(client.post("/suppliers", json=payload[i]))
        assert create_resp[i].status_code == 201
        supplier_id.append(create_resp[i].get_json()["id"])

    # Get all suppliers in /suppliers with GET
    supplier_resp = client.get("/suppliers")

    # Ensure GET has worked
    assert supplier_resp.status_code == 200
    suppliers = supplier_resp.get_json()
    assert len(suppliers) == len(payload)

    # Ensure the supplier was retrieved correctly
    for i in range(len(suppliers)):
        assert suppliers[i]["name"] == payload[i]["name"]
        assert suppliers[i]["contact_email"] == payload[i]["contact_email"]