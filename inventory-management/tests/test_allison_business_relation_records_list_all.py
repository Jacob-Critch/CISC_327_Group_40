def test_list_business_relation_records_returns_empty_list_initially(client):
    """business_relation_records endpoint returns an empty list when no business_relation_records have been added."""
    response = client.get("/business_relation_records")
    assert response.status_code == 200
    assert response.get_json() == []

def test_business_relation_record_create_business_relation_records_then_list_all(client):
    """All business relation records POSTed to /business_relation_records can be retrieved as an array with GET"""

    # Define business_relation_records to be POSTed
    record_1 = {
        "supplier_id": "Supplier 1",
        "quantity_deliveries": "test@test.test",
    }
    record_2 = {
        "supplier_id": "supplier 2",
        "quantity_deliveries": "test2@test.test",
    }
    payload = [record_1, record_2]

    # POST business relation records
    create_resp = []
    record_id = []
    for i in range(len(payload)):
        create_resp.append(client.post("/business_relation_records", json=payload[i]))
        assert create_resp[i].status_code == 201
        record_id.append(create_resp[i].get_json()["id"])

    # Get all business relation_records in /business_relation_records with GET
    business_relation_record_resp = client.get("/business_relation_records")

    # Ensure GET has worked
    assert business_relation_record_resp.status_code == 200
    business_relation_records = business_relation_record_resp.get_json()
    assert len(business_relation_records) == len(payload)

    # Ensure the business_relation_record was retrieved correctly
    for i in range(len(business_relation_records)):
        assert business_relation_records[i]["supplier_id"] == payload[i]["supplier_id"]
        assert business_relation_records[i]["quantity_deliveries"] == payload[i]["quantity_deliveries"]