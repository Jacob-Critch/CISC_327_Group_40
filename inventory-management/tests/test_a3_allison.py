## Tests app/routes/products.py
#Tests for the send_stock_alert(product_id) function

import notification_service
import app.store as store

def test_notification_service_offline_returns_404(client):
    """Attempting to use send_stock_alert(product_id) while service is offline returns a status code of 404 and an error message"""
    notification_service.clear_notifications()

    notification_service.set_available(False)
    product_id = 0

    response = client.post(f"/products/send-stock-alert/{product_id}")

    assert response.status_code == 404
    message = response.get_json()
    if message == None:
        assert False
    else:
        assert message['error'] == "Notification service is offline."
    assert notification_service.get_notifications() == []

def test_notification_service_online_valid_product_id_sends_notification_and_returns_200(client):
    """Attempting to use send_stock_alert(product_id) while service is online and product_id is valid sends a message, returns a status code of 200, and returns a message"""
    notification_service.clear_notifications()

    response = client.post("/products", json = {"name": "Product", "quantity_on_hand": 2, "reorder_level": 2, "sku": "A", "unit_price": 1})
    assert response.status_code == 201
    product = response.get_json()
    assert product['id'] == 1
    assert product['is_below_reorder_level'] == False
    assert product['name'] == "Product"
    assert product['quantity_on_hand'] == 2
    assert product['reorder_level'] == 2
    assert product['sku'] == "A"
    assert product['unit_price'] == 1
    
    response = client.post(f"/products/send-stock-alert/{product['id']}")
    assert response.status_code == 200

    response = notification_service.get_notifications()
    assert response != []
    assert response[0]['recipient'] == store.ADMIN_EMAILS[0]
    assert response[0]['subject'] == "Stock alert"
    assert response[0]['message'] == f"Stock alert for {product['name']} ({product['id']}): {product['reorder_level'] - product['quantity_on_hand']} more are needed to restore target levels."
    

def test_notification_service_online_invalid_product_id_returns_404(client):
    """Attempting to use send_stock_alert(product_id) while service is online, but the produc_id is invalid does not send a message, returns a status code of 404, and returns an error message"""
    notification_service.clear_notifications()
    
    response = client.post(f"/products/send-stock-alert/0")
    assert response.status_code == 404
    message = response.get_json()
    if message == None:
        assert False
    else:
        assert message['error'] == "Product not found"

    response = notification_service.get_notifications()
    assert response == []

#Test for the get_business_relation_record_id(business_relation_record_id) function in app/routes/business_relation_records.py
def test_business_relation_record_get_invalid_id_get_returns_404_error(client):
    """Attempting to use get_business_relation_record_id(business_relation_record_id) with an invalid ID returns a 404 error"""
    response = client.get("/business_relation_records/0")
    assert response.status_code == 404
    record = response.get_json()
    assert record['error'] == "Record not found"

#Tests for the delete_business_relation_record(business_relation_record_id) function in app/routes/business_relation_records.py
def test_business_relation_record_delete_valid_record_deletes_and_returns_200(client):
    response = client.post("/business_relation_records", json = {"supplier_id": 1, "quantity_deliveries": 1})
    assert response.status_code == 201
    record = response.get_json()
    assert record['id'] == 1

    response = client.delete("/business_relation_records/1")
    assert response.status_code == 200
    record = response.get_json()
    assert record['message'] == "Record ID 1 was deleted"

def test_business_relation_record_delete_invalid_record_returns_404_error(client):
    response = client.delete("/business_relation_records/0")
    assert response.status_code == 404
    record = response.get_json()
    assert record['error'] == "Record not found"

## Tests app/routes/views.py
#Tests for the home() function
def test_home_returns_render_template(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "<!doctype html>" in response.get_data(as_text=True)
    assert "<title>Inventory Management System</title>" in response.get_data(as_text=True)
    assert response.location == None

#Tests for the products_page() function
def tests_products_page_post_adds_product_and_returns_products_page_with_products_listed(client):
    get_empty = client.get("/ui/products", follow_redirects=True)

    payload = {
        "name" : "Test product",
        "sku" : "1",
        "unit_price": 1.0,
        "quantity_on_hand": 1,
    }

    response = client.post("/ui/products", data=payload)
    assert response.status_code == 302
    assert response.location == "/ui/products"

    response = client.get("/ui/products")
    assert response != get_empty
    assert payload['name'] in response.get_data(as_text=True)

def test_products_page_post_invalid_product_only_returns_redirect_to_product_page(client):
    response_1 = client.get("/ui/products")

    payload={}

    response_2 = client.post("/ui/products", data=payload)
    assert response_2.status_code == 400

    response_3 = client.get("/ui/products")
    assert response_1.get_data() == response_3.get_data()

def tests_products_page_get_returns_products_page_with_products_listed(client):
    response = client.get("/ui/products")
    assert response.status_code == 200
    assert "<title>Inventory Management System</title>" in response.get_data(as_text=True)
    assert "<h1>Products</h1>" in response.get_data(as_text=True)


#Tests for the delete_product_page(product_id) function
def tests_product_page_delete_removes_valid_product_returns_redirect_to_products_page(client):
    payload = {
        "name" : "Test product",
        "sku" : "1",
        "unit_price": 1.0,
        "quantity_on_hand": 1,
    }
    
    response = client.post("/ui/products", data=payload)
    assert response.status_code == 302
    assert response.location == "/ui/products"

    response = client.get("/ui/products")
    assert payload['name'] in response.get_data(as_text=True)

    response = client.post("/ui/products/1/delete", follow_redirects=True)
    assert payload['name'] not in response.get_data(as_text=True)

def tests_product_page_delete_invalid_product_returns_only_redirect_to_products_page(client):
    response_1 = client.get("/ui/products")

    response_2 = client.post("/ui/products/0/delete", follow_redirects=True)
    assert response_2.status_code == 200

    response_3 = client.get("/ui/products")
    assert response_1.get_data() == response_3.get_data()

#Tests for the suppliers_page() function
def tests_suppliers_page_post_adds_product_and_returns_suppliers_page_with_suppliers_listed(client):
    get_empty = client.get("/ui/suppliers", follow_redirects=True)

    payload = {
        "name" : "Test Supplier",
        "contact_email": "supplieremail@email.email"
    }

    response = client.post("/ui/suppliers", data=payload)
    assert response.status_code == 302
    assert response.location == "/ui/suppliers"

    response = client.get("/ui/suppliers")
    assert response != get_empty
    assert payload['name'] in response.get_data(as_text=True)
    assert payload['contact_email'] in response.get_data(as_text=True)

def test_suppliers_page_post_invalid_supplier_only_returns_redirect_to_supplier_page(client):
    response_1 = client.get("/ui/suppliers")

    payload={}

    response_2 = client.post("/ui/suppliers", data=payload)
    assert response_2.status_code == 400

    response_3 = client.get("/ui/suppliers")
    assert response_1.get_data() == response_3.get_data()

def tests_suppliers_page_get_returns_suppliers_page_with_suppliers_listed(client):
    response = client.get("/ui/suppliers")
    assert response.status_code == 200
    assert "<title>Inventory Management System</title>" in response.get_data(as_text=True)
    assert "<h1>Suppliers</h1>" in response.get_data(as_text=True)

#Tests for the delete_supplier_page(supplier_id) function
def tests_supplier_page_delete_removes_valid_supplier_returns_redirect_to_suppliers_page(client):
    payload = {
            "name" : "Test Supplier",
            "contact_email": "supplieremail@email.email"
    }
    
    response = client.post("/ui/suppliers", data=payload)
    assert response.status_code == 302
    assert response.location == "/ui/suppliers"

    response = client.get("/ui/suppliers")
    assert payload['name'] in response.get_data(as_text=True)

    response = client.delete("/ui/suppliers/1/delete", follow_redirects=True)
    assert payload['name'] not in response.get_data(as_text=True)

def tests_supplier_page_delete_invalid_supplier_returns_only_redirect_to_suppliers_page(client):
    response_1 = client.get("/ui/suppliers")
    
    response_2 = client.delete("/ui/suppliers/0/delete", follow_redirects=True)
    assert response_2.status_code == 200
    
    response_3 = client.get("/ui/suppliers")
    assert response_1.get_data() == response_3.get_data()

#Tests for the transaction_page() function
def test_transaction_page_post_valid_transaction_posts_transaction_and_returns_redirect_to_transaction_page(client):
    for i in range(2):
        payload = {
            "name" : "Test product",
            "sku" : "1",
            "unit_price": 1.0,
            "quantity_on_hand": 1,
        }
        
        response = client.post("/ui/products", data=payload)
        assert response.status_code == 302
        assert response.location == "/ui/products"
        
        payload = {
            "name" : "Test Supplier",
            "contact_email": "supplieremail@email.email"
        }

        response = client.post("/ui/suppliers", data=payload)
        assert response.status_code == 302
        assert response.location == "/ui/suppliers"

        get_empty = client.get("/ui/transactions", follow_redirects=True)

        if i == 0:
            type_payload = "IN"
        else:
            type_payload = "OUT"


        payload = {
            "product_id" : 1,
            "type" : type_payload,
            "quantity": 1,
            "supplier_id": 1,
        }

        response = client.post("/ui/transactions", data=payload)
        assert response.status_code == 302
        assert response.location == "/ui/transactions"

        response = client.get("/ui/transactions")
        assert response != get_empty
        assert str(payload['product_id']) in response.get_data(as_text=True)
        assert payload['type'] in response.get_data(as_text=True)
        assert str(payload['quantity']) in response.get_data(as_text=True)
        assert str(payload['supplier_id']) in response.get_data(as_text=True)

def test_transactions_page_post_invalid_transactions_only_returns_redirect_to_transactions_page(client):
    response_1 = client.get("/ui/transactions")

    payload={}

    response_2 = client.post("/ui/transactions", data=payload)
    assert response_2.status_code == 400

    response_3 = client.get("/ui/transactions")
    assert response_1.get_data() == response_3.get_data()

def tests_transaction_page_get_returns_transactions_page_with_transactions_listed(client):
    response = client.get("/ui/transactions")
    assert response.status_code == 200
    assert "<title>Inventory Management System</title>" in response.get_data(as_text=True)
    assert "<h1>Transactions</h1>" in response.get_data(as_text=True)

#Tests for the business_relation_records_page() function
def test_business_relation_records_page_get_generates_and_returns_redirect_to_transaction_page(client):
    original_response = client.get("/ui/business_relation_records")
    assert original_response.status_code == 200
    assert "<title>Inventory Management System</title>" in original_response.get_data(as_text=True)
    assert "<h1>Business Relation Records</h1>" in original_response.get_data(as_text=True)

    payload = {
        "name" : "Test product",
        "sku" : "1",
        "unit_price": 1.0,
        "quantity_on_hand": 1,
    }
    
    response = client.post("/ui/products", data=payload)
    assert response.status_code == 302
    assert response.location == "/ui/products"
    
    payload = {
        "name" : "Test Supplier",
        "contact_email": "supplieremail@email.email"
    }

    response = client.post("/ui/suppliers", data=payload)
    assert response.status_code == 302
    assert response.location == "/ui/suppliers"

    payload = {
        "product_id" : 1,
        "type" : "IN",
        "quantity": 1,
        "supplier_id": 1,
    }

    response = client.post("/ui/transactions", data=payload)
    assert response.status_code == 302
    assert response.location == "/ui/transactions"

    response = client.get("/ui/business_relation_records")
    assert response.status_code == 200
    assert "<title>Inventory Management System</title>" in response.get_data(as_text=True)
    assert "<h1>Business Relation Records</h1>" in response.get_data(as_text=True)
    assert original_response != response
