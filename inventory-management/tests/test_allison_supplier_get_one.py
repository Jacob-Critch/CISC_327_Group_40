def test_supplier_get_nonexistent_supplier_returns_404(client):
    """Attempting to GET a supplier that does not exist responds with HTTP 404"""

    id_invalid = -1

    response = client.get(f"/suppliers/{id_invalid}")
    assert response.status_code == 404

def test_supplier_create_and_check_get_one_returns(client):
    """A supplier POSTed to /suppliers results can be retrieved with GET"""

    payload = {
        "name": "Supplier 1",
        "contact_email": "test@test.test",
    }
    create_resp = client.post("/suppliers", json=payload)
    assert create_resp.status_code == 201
    supplier_id = create_resp.get_json()["id"]

    supplier_resp = client.get(f"/suppliers/{supplier_id}")
    assert supplier_resp.status_code == 200
    supplier = supplier_resp.get_json()

    assert supplier["name"] == payload["name"]
    assert supplier["contact_email"] == payload["contact_email"]