def test_business_relation_record_get_nonexistent_business_relation_record_returns_404(client):
    """Attempting to GET a business_relation_record that does not exist responds with HTTP 404"""

    id_invalid = -1

    response = client.get(f"/business_relation_records/{id_invalid}")
    assert response.status_code == 404

def test_business_relation_record_create_and_check_get_one_returns(client):
    """A business_relation_record POSTed to /business_relation_records results can be retrieved with GET"""

    payload = {
        "supplier_id": 1,
        "quantity_deliveries": 10,
    }
    create_resp = client.post("/business_relation_records", json=payload)
    assert create_resp.status_code == 201
    business_relation_record_id = create_resp.get_json()["id"]

    business_relation_record_resp = client.get(f"/business_relation_records/{business_relation_record_id}")
    assert business_relation_record_resp.status_code == 200
    business_relation_record = business_relation_record_resp.get_json()

    assert business_relation_record["supplier_id"] == payload["supplier_id"]
    assert business_relation_record["quantity_deliveries"] == payload["quantity_deliveries"]