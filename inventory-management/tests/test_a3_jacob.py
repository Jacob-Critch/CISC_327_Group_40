from datetime import date
from app.models.purchase_order import PurchaseOrder

# TEST 1: app/models/purchase_order.py

# TEST 1A: Trivial Case (Lines 15-21, 24)
def test_purchase_order_trivial_case_lines_15_to_21_and_24():
    purchaseOrder = PurchaseOrder(id = 1, supplier_id = 1, product_id = 1, quantity_ordered = 1)   
    
    purchaseOrderDictionary = purchaseOrder.to_dict()
    assert purchaseOrderDictionary["id"] == 1
    assert purchaseOrderDictionary["supplier_id"] == 1
    assert purchaseOrderDictionary["product_id"] == 1
    assert purchaseOrderDictionary["quantity_ordered"] == 1
    assert purchaseOrderDictionary["status"] == "pending"
    assert purchaseOrderDictionary["created_date"] == date.today().isoformat()
    assert purchaseOrderDictionary["received_date"] == None

# TEST 1B: Non-Empty received_date Alternative Case (Lines 15-21, 24)
def test_purchase_order_nonempty_received_date_alternative_case_lines_15_to_21_and_24():
    purchaseOrder = PurchaseOrder(id = 1, supplier_id = 1, product_id = 1, quantity_ordered = 1, received_date = date.today())   
    
    purchaseOrderDictionary = purchaseOrder.to_dict()
    assert purchaseOrderDictionary["id"] == 1
    assert purchaseOrderDictionary["supplier_id"] == 1
    assert purchaseOrderDictionary["product_id"] == 1
    assert purchaseOrderDictionary["quantity_ordered"] == 1
    assert purchaseOrderDictionary["status"] == "pending"
    assert purchaseOrderDictionary["created_date"] == date.today().isoformat()
    assert purchaseOrderDictionary["received_date"] == date.today().isoformat()

# TEST 1C: Empty Arguments Failure Case
def test_purchase_order_empty_arguments_failure_case():
    try:
        PurchaseOrder()
    except:
        assert True
        return
    assert False

# TEST 2: app/routes/products.py

# TEST 2A: Trivial Case (Lines 17-21)
def test_products_trivial_case_lines_17_to_21(client):
    productPost = client.post("/products", json = {"name": "Product", "quantity_on_hand": 1, "reorder_level": 1, "sku": "A", "unit_price": 1})
    assert productPost.status_code == 201

    productJson = productPost.get_json()
    assert productJson["id"] == 1
    assert productJson["name"] == "Product"
    assert productJson["quantity_on_hand"] == 1
    assert productJson["reorder_level"] == 1
    assert productJson["sku"] == "A"
    assert productJson["unit_price"] == 1 
    
    lowStockGet = client.get("/products/low-stock")
    assert lowStockGet.status_code == 200

    lowStockJson = lowStockGet.get_json()
    assert lowStockJson[0]["id"] == 1
    assert lowStockJson[0]["name"] == "Product"
    assert lowStockJson[0]["quantity_on_hand"] == 1
    assert lowStockJson[0]["reorder_level"] == 1
    assert lowStockJson[0]["sku"] == "A"
    assert lowStockJson[0]["unit_price"] == 1

# TEST 2B: Two Low Stocks Alternative Case (Lines 17-21)
def test_products_two_low_stocs_alrternative_case_lines_17_to_21(client):
    productPost1 = client.post("/products", json = {"name": "Product 1", "quantity_on_hand": 1, "reorder_level": 1, "sku": "A", "unit_price": 1})
    assert productPost1.status_code == 201
    
    productJson1 = productPost1.get_json()
    assert productJson1["id"] == 1
    assert productJson1["name"] == "Product 1"
    assert productJson1["quantity_on_hand"] == 1
    assert productJson1["reorder_level"] == 1
    assert productJson1["sku"] == "A"
    assert productJson1["unit_price"] == 1 

    productPost2 = client.post("/products", json = {"name": "Product 2", "quantity_on_hand": 2, "reorder_level": 2, "sku": "B", "unit_price": 2})
    assert productPost2.status_code == 201

    productJson2 = productPost2.get_json()
    assert productJson2["id"] == 2
    assert productJson2["name"] == "Product 2"
    assert productJson2["quantity_on_hand"] == 2
    assert productJson2["reorder_level"] == 2
    assert productJson2["sku"] == "B"
    assert productJson2["unit_price"] == 2

    lowStockGet = client.get("/products/low-stock")
    assert lowStockGet.status_code == 200

    lowStockJson = lowStockGet.get_json()
    assert lowStockJson[0]["id"] == 1
    assert lowStockJson[0]["name"] == "Product 1"
    assert lowStockJson[0]["quantity_on_hand"] == 1
    assert lowStockJson[0]["reorder_level"] == 1
    assert lowStockJson[0]["sku"] == "A"
    assert lowStockJson[0]["unit_price"] == 1
    assert lowStockJson[1]["id"] == 2
    assert lowStockJson[1]["name"] == "Product 2"
    assert lowStockJson[1]["quantity_on_hand"] == 2
    assert lowStockJson[1]["reorder_level"] == 2
    assert lowStockJson[1]["sku"] == "B"
    assert lowStockJson[1]["unit_price"] == 2

# TEST 2C: No Low Stock Alternative Case (Lines 17-21)
def test_products_no_low_stock_alternative_case_lines_17_to_21(client):
    productPost = client.post("/products", json = {"name": "Product", "quantity_on_hand": 2, "reorder_level": 1, "sku": "A", "unit_price": 1})
    assert productPost.status_code == 201
    
    productJson = productPost.get_json()
    assert productJson["id"] == 1
    assert productJson["name"] == "Product"
    assert productJson["quantity_on_hand"] == 2
    assert productJson["reorder_level"] == 1
    assert productJson["sku"] == "A"
    assert productJson["unit_price"] == 1 
        
    lowStockGet = client.get("/products/low-stock")
    assert lowStockGet.status_code == 200
    
    lowStockJson = lowStockGet.get_json()
    assert lowStockJson == list()

# TEST 2D: Empty Product Update Failure Case (Line 52)
def test_products_empty_product_update_failure_case_line_52(client):
    productPut = client.put("/products/1", json = {"name": "Input", "quantity_on_hand": 2, "reorder_level": 2, "sku": "B", "unit_price": 2})
    assert productPut.status_code == 404

    updateJson = productPut.get_json()
    assert updateJson["error"] == "Product not found"

# TEST 2E: Empty Product Delete Failure Case (Line 66)
def test_products_empty_product_delete_failure_case_line_66(client):
    productDelete = client.delete("/products/1")
    assert productDelete.status_code == 404

    deleteJson = productDelete.get_json()
    assert deleteJson["error"] == "Product not found"

# TEST 2F: Empty Product Stock Level Access Failure Case (Line 74)
def test_products_empty_product_stock_level_Access_failure_case_line_74(client):
    productGet = client.get("/products/1/stock-level")
    assert productGet.status_code == 404

    accessJson = productGet.get_json()
    assert accessJson["error"] == "Product not found"
