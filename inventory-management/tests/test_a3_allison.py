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
        assert message["error"] == "Notification service is offline."
    assert notification_service.get_notifications() == []

def test_notification_service_online_admin_valid_message_returns_200(client):
    """Attempting to use send_stock_alert(product_id) while service is online and product_id is valid sends a message, returns a status code of 200, and returns a message"""
    notification_service.clear_notifications()

    response = client.post("/products", json = {"name": "Product", "quantity_on_hand": 2, "reorder_level": 2, "sku": "A", "unit_price": 1})
    assert response.status_code == 201
    product = response.get_json()
    assert product["id"] == 1
    assert product["is_below_reorder_level"] == False
    assert product["name"] == "Product"
    assert product["quantity_on_hand"] == 2
    assert product["reorder_level"] == 2
    assert product["sku"] == "A"
    assert product["unit_price"] == 1
    
    response = client.post(f"/products/send-stock-alert/{product["id"]}")
    assert response.status_code == 200

    response = notification_service.get_notifications()
    assert response != []
    assert response[0]["recipient"] == store.ADMIN_EMAILS[0]
    assert response[0]["subject"] == "Stock alert"
    assert response[0]["message"] == f"Stock alert for {product["name"]} ({product["id"]}): {product["reorder_level"] - product["quantity_on_hand"]} more are needed to restore target levels."
    

def test_notification_service_online_invalid_product_id_returns_404(client):
    """Attempting to use send_stock_alert(product_id) while service is online, but the produc_id is invalid does not send a message, returns a status code of 404, and returns an error message"""
    notification_service.clear_notifications()
    
    response = client.post(f"/products/send-stock-alert/0")
    assert response.status_code == 404
    message = response.get_json()
    if message == None:
        assert False
    else:
        assert message["error"] == "Product not found"

    response = notification_service.get_notifications()
    assert response == []