def test_supplier_delete_nonexistent_supplier_returns_404(client):
    """Attempting to DELETE a supplier that does not exist responds with HTTP 404"""

    id_invalid = -1

    response = client.delete(f"/suppliers/{id_invalid}")
    assert response.status_code == 404

def test_supplier_create_and_then_delete(client):
    """A supplier POSTed to /suppliers results can be deleted with GET"""

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

    supplier_resp = client.delete(f"/suppliers/{supplier_id}")
    assert (supplier_resp.status_code == 200 or supplier_resp.status_code == 204)

    supplier_resp = client.get(f"/suppliers/{supplier_id}")
    assert supplier_resp.status_code == 404