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
    productsPost = client.post("/products", json = {"name": "Product", "quantity_on_hand": 1, "reorder_level": 1, "sku": "A", "unit_price": 1})
    assert productsPost.status_code == 201

    productJson = productsPost.get_json()
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
    productsPost1 = client.post("/products", json = {"name": "Product 1", "quantity_on_hand": 1, "reorder_level": 1, "sku": "A", "unit_price": 1})
    assert productsPost1.status_code == 201
    
    productJson1 = productsPost1.get_json()
    assert productJson1["id"] == 1
    assert productJson1["name"] == "Product 1"
    assert productJson1["quantity_on_hand"] == 1
    assert productJson1["reorder_level"] == 1
    assert productJson1["sku"] == "A"
    assert productJson1["unit_price"] == 1 

    productsPost2 = client.post("/products", json = {"name": "Product 2", "quantity_on_hand": 2, "reorder_level": 2, "sku": "B", "unit_price": 2})
    assert productsPost2.status_code == 201

    productJson2 = productsPost2.get_json()
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
    productsPost = client.post("/products", json = {"name": "Product", "quantity_on_hand": 2, "reorder_level": 1, "sku": "A", "unit_price": 1})
    assert productsPost.status_code == 201
    
    productJson = productsPost.get_json()
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
    productsPut = client.put("/products/1", json = {"name": "Input", "quantity_on_hand": 2, "reorder_level": 2, "sku": "B", "unit_price": 2})
    assert productsPut.status_code == 404

    updateJson = productsPut.get_json()
    assert updateJson["error"] == "Product not found"

# TEST 2E: Empty Product Delete Failure Case (Line 66)
def test_products_empty_product_delete_failure_case_line_66(client):
    productsDelete = client.delete("/products/1")
    assert productsDelete.status_code == 404

    deleteJson = productsDelete.get_json()
    assert deleteJson["error"] == "Product not found"

# TEST 2F: Empty Product Stock Level Access Failure Case (Line 74)
def test_products_empty_product_stock_level_Access_failure_case_line_74(client):
    productsGet = client.get("/products/1/stock-level")
    assert productsGet.status_code == 404

    accessJson = productsGet.get_json()
    assert accessJson["error"] == "Product not found"

# TEST 3: app/routes/purchase_orders.py

# TEST 3A: Trivial Case (Line 14)
def test_purchase_orders_trivial_case_line_14(client):
    productsPost = client.post("/products", json = {"name": "Product", "quantity_on_hand": 1, "reorder_level": 1, "sku": "A", "unit_price": 1})
    assert productsPost.status_code == 201
        
    productJson = productsPost.get_json()
    assert productJson["id"] == 1
    assert productJson["name"] == "Product"
    assert productJson["quantity_on_hand"] == 1
    assert productJson["reorder_level"] == 1
    assert productJson["sku"] == "A"
    assert productJson["unit_price"] == 1 
    
    suppliersPost = client.post("/suppliers", json = {"contact_email": "johndoe@email.com", "name": "Supplier"})
    assert suppliersPost.status_code == 201
    
    supplierJSON = suppliersPost.get_json()
    assert supplierJSON["contact_email"] == "johndoe@email.com"
    assert supplierJSON["id"] == 1
    assert supplierJSON["name"] == "Supplier"
    
    purchaseOrdersPost = client.post("/purchase-orders", json = {"product_id": 1, "quantity_ordered": 1, "supplier_id": 1})
    assert purchaseOrdersPost.status_code == 201

    purchaseOrderJson = purchaseOrdersPost.get_json()
    assert purchaseOrderJson["created_date"] == date.today().isoformat()
    assert purchaseOrderJson["id"] == 1
    assert purchaseOrderJson["product_id"] == 1
    assert purchaseOrderJson["quantity_ordered"] == 1
    assert purchaseOrderJson["received_date"] == None
    assert purchaseOrderJson["status"] == "pending"
    assert purchaseOrderJson["supplier_id"] == 1

    purchaseOrdersGet = client.get("/purchase-orders")
    assert purchaseOrdersGet.status_code == 200

    purchaseOrdersJson = purchaseOrdersGet.get_json()
    assert purchaseOrdersJson[0]["created_date"] == date.today().isoformat()
    assert purchaseOrdersJson[0]["id"] == 1
    assert purchaseOrdersJson[0]["product_id"] == 1
    assert purchaseOrdersJson[0]["quantity_ordered"] == 1
    assert purchaseOrdersJson[0]["received_date"] == None
    assert purchaseOrdersJson[0]["status"] == "pending"
    assert purchaseOrdersJson[0]["supplier_id"] == 1

# TEST 3B: Two Purchase Orders Alternative Case (Line 14)
def test_purhcase_orders_two_purchaes_orders_alternative_case_line_14(client):
    productsPost1 = client.post("/products", json = {"name": "Product 1", "quantity_on_hand": 1, "reorder_level": 1, "sku": "A", "unit_price": 1})
    assert productsPost1.status_code == 201
     
    productJson1 = productsPost1.get_json()
    assert productJson1["id"] == 1
    assert productJson1["name"] == "Product 1"
    assert productJson1["quantity_on_hand"] == 1
    assert productJson1["reorder_level"] == 1
    assert productJson1["sku"] == "A"
    assert productJson1["unit_price"] == 1

    productsPost2 = client.post("/products", json = {"name": "Product 2", "quantity_on_hand": 2, "reorder_level": 2, "sku": "B", "unit_price": 2})
    assert productsPost2.status_code == 201
            
    productJson2 = productsPost2.get_json()
    assert productJson2["id"] == 2
    assert productJson2["name"] == "Product 2"
    assert productJson2["quantity_on_hand"] == 2
    assert productJson2["reorder_level"] == 2
    assert productJson2["sku"] == "B"
    assert productJson2["unit_price"] == 2

    suppliersPost1 = client.post("/suppliers", json = {"contact_email": "johndoe@email.com", "name": "Supplier"})
    assert suppliersPost1.status_code == 201

    supplierJSON1 = suppliersPost1.get_json()
    assert supplierJSON1["contact_email"] == "johndoe@email.com"
    assert supplierJSON1["id"] == 1
    assert supplierJSON1["name"] == "Supplier"

    suppliersPost2 = client.post("/suppliers", json = {"contact_email": "janedoe@email.com", "name": "Buyer"})
    assert suppliersPost2.status_code == 201

    supplierJSON2 = suppliersPost2.get_json()
    assert supplierJSON2["contact_email"] == "janedoe@email.com"
    assert supplierJSON2["id"] == 2
    assert supplierJSON2["name"] == "Buyer"

    purchaseOrdersPost1 = client.post("/purchase-orders", json = {"product_id": 1, "quantity_ordered": 1, "supplier_id": 1})
    assert purchaseOrdersPost1.status_code == 201
    
    purchaseOrderJson1 = purchaseOrdersPost1.get_json()
    assert purchaseOrderJson1["created_date"] == date.today().isoformat()
    assert purchaseOrderJson1["id"] == 1
    assert purchaseOrderJson1["product_id"] == 1
    assert purchaseOrderJson1["quantity_ordered"] == 1
    assert purchaseOrderJson1["received_date"] == None
    assert purchaseOrderJson1["status"] == "pending"
    assert purchaseOrderJson1["supplier_id"] == 1

    purchaseOrdersPost2 = client.post("/purchase-orders", json = {"product_id": 2, "quantity_ordered": 2, "supplier_id": 2})
    assert purchaseOrdersPost2.status_code == 201

    purchaseOrderJson2 = purchaseOrdersPost2.get_json()
    assert purchaseOrderJson2["created_date"] == date.today().isoformat()
    assert purchaseOrderJson2["id"] == 2
    assert purchaseOrderJson2["product_id"] == 2
    assert purchaseOrderJson2["quantity_ordered"] == 2
    assert purchaseOrderJson2["received_date"] == None
    assert purchaseOrderJson2["status"] == "pending"
    assert purchaseOrderJson2["supplier_id"] == 2

    purchaseOrdersGet = client.get("/purchase-orders")
    assert purchaseOrdersGet.status_code == 200

    purchaseOrdersJson = purchaseOrdersGet.get_json()
    assert purchaseOrdersJson[0]["created_date"] == date.today().isoformat()
    assert purchaseOrdersJson[0]["id"] == 1
    assert purchaseOrdersJson[0]["product_id"] == 1
    assert purchaseOrdersJson[0]["quantity_ordered"] == 1
    assert purchaseOrdersJson[0]["received_date"] == None
    assert purchaseOrdersJson[0]["status"] == "pending"
    assert purchaseOrdersJson[0]["supplier_id"] == 1
    assert purchaseOrdersJson[1]["created_date"] == date.today().isoformat()
    assert purchaseOrdersJson[1]["id"] == 2
    assert purchaseOrdersJson[1]["product_id"] == 2
    assert purchaseOrdersJson[1]["quantity_ordered"] == 2
    assert purchaseOrdersJson[1]["received_date"] == None
    assert purchaseOrdersJson[1]["status"] == "pending"
    assert purchaseOrdersJson[1]["supplier_id"] == 2

# TEST 3C: No Purchase Order Alternative Case (Line 14)
def test_purchase_orders_no_purchase_order_alternative_case_line_14(client):
    purchaseOrdersGet = client.get("/purchase-orders")
    assert purchaseOrdersGet.status_code == 200

    purchaseOrdersJson = purchaseOrdersGet.get_json()
    assert purchaseOrdersJson == list()

# TEST 3D: Trivial Case (Lines 19-21, 23-24, 26-36))
def test_purchase_orders_trivial_case_lines_19_to_21_and_23_to_24_and_26_to_36(client):
    productsPost = client.post("/products", json = {"name": "Product", "quantity_on_hand": 1, "reorder_level": 1, "sku": "A", "unit_price": 1})
    assert productsPost.status_code == 201
        
    productJson = productsPost.get_json()
    assert productJson["id"] == 1
    assert productJson["name"] == "Product"
    assert productJson["quantity_on_hand"] == 1
    assert productJson["reorder_level"] == 1
    assert productJson["sku"] == "A"
    assert productJson["unit_price"] == 1 
    
    suppliersPost = client.post("/suppliers", json = {"contact_email": "johndoe@email.com", "name": "Supplier"})
    assert suppliersPost.status_code == 201
    
    supplierJSON = suppliersPost.get_json()
    assert supplierJSON["contact_email"] == "johndoe@email.com"
    assert supplierJSON["id"] == 1
    assert supplierJSON["name"] == "Supplier"
    
    purchaseOrdersPost = client.post("/purchase-orders", json = {"product_id": 1, "quantity_ordered": 1, "supplier_id": 1})
    assert purchaseOrdersPost.status_code == 201

    createJson = purchaseOrdersPost.get_json()
    assert createJson["created_date"] == date.today().isoformat()
    assert createJson["id"] == 1
    assert createJson["product_id"] == 1
    assert createJson["quantity_ordered"] == 1
    assert createJson["received_date"] == None
    assert createJson["status"] == "pending"
    assert createJson["supplier_id"] == 1

# Test 3E: Empty Supplier Failure Case (Line 22)
def test_purchase_orders_empty_supplier_failure_case_line_22(client):
    productsPost = client.post("/products", json = {"name": "Product", "quantity_on_hand": 1, "reorder_level": 1, "sku": "A", "unit_price": 1})
    assert productsPost.status_code == 201
        
    productJson = productsPost.get_json()
    assert productJson["id"] == 1
    assert productJson["name"] == "Product"
    assert productJson["quantity_on_hand"] == 1
    assert productJson["reorder_level"] == 1
    assert productJson["sku"] == "A"
    assert productJson["unit_price"] == 1

    purchaseOrdersPost = client.post("/purchase-orders", json = {"product_id": 1, "quantity_ordered": 1, "supplier_id": 1})
    assert purchaseOrdersPost.status_code == 404
    
    createJson = purchaseOrdersPost.get_json()
    assert createJson["error"] == "Supplier not found"

# TEST 3F: Empty product Failure Case (Line 25)
def test_purchase_orders_empty_product__failure_case_line_25(client):
    suppliersPost = client.post("/suppliers", json = {"contact_email": "johndoe@email.com", "name": "Supplier"})
    assert suppliersPost.status_code == 201
    
    supplierJSON = suppliersPost.get_json()
    assert supplierJSON["contact_email"] == "johndoe@email.com"
    assert supplierJSON["id"] == 1
    assert supplierJSON["name"] == "Supplier"

    purchaseOrdersPost = client.post("/purchase-orders", json = {"product_id": 1, "quantity_ordered": 1, "supplier_id": 1})
    assert purchaseOrdersPost.status_code == 404
        
    createJson = purchaseOrdersPost.get_json()
    assert createJson["error"] == "Product not found"

# TEST 4: app/routes/suppliers.py

# TEST 4A: Empty Supplier Update Failure Case (Line 35)
def test_suppliers_empty_supplier_update_failure_case_line_35(client):
    suppliersPut = client.put("/suppliers/1", json = {"contact_email": "janedoe@email.com", "name": "Buyer"})
    assert suppliersPut.status_code == 404

    updateJson = suppliersPut.get_json()
    assert updateJson["error"] == "Supplier not found"

# TEST 4B: Empty Supplier Delete Failure Case (Line 46)
def test_suppliers_empty_supplier_delete_failure_case_line_46(client):
    suppliersDelete = client.delete("/suppliers/1")
    assert suppliersDelete.status_code == 404

    deleteJson = suppliersDelete.get_json()
    assert deleteJson["error"] == "Supplier not found"

# TEST 4C: Trivial Case (Lines 53-54, 56-67)
def test_suppliers_trivial_case_lines_53_to_54_and_56_to_67(client):
    productsPost = client.post("/products", json = {"name": "Product", "quantity_on_hand": 1, "reorder_level": 1, "sku": "A", "unit_price": 1})
    assert productsPost.status_code == 201
    
    productJson = productsPost.get_json()
    assert productJson["id"] == 1
    assert productJson["name"] == "Product"
    assert productJson["quantity_on_hand"] == 1
    assert productJson["reorder_level"] == 1
    assert productJson["sku"] == "A"
    assert productJson["unit_price"] == 1

    suppliersPost = client.post("/suppliers", json = {"contact_email": "johndoe@email.com", "name": "Supplier"})
    assert suppliersPost.status_code == 201

    supplierJSON = suppliersPost.get_json()
    assert supplierJSON["contact_email"] == "johndoe@email.com"
    assert supplierJSON["id"] == 1
    assert supplierJSON["name"] == "Supplier"
        
    transactionsPost = client.post("/transactions", json = {"product_id": 1, "quantity": 1, "supplier_id": 1, "type": "IN"})
    assert transactionsPost.status_code == 201
    
    transactionJSON = transactionsPost.get_json()
    transactionJSON["product_id"] == 1
    transactionJSON["quantity"] == 1
    transactionJSON["supplier_id"] == 1
    transactionJSON["transaction_date"] == date.today().isoformat()
    transactionJSON["type"] == "IN"

    transactionsGet = client.get("/suppliers/1/products")
    assert transactionsGet.status_code == 200

    productsJson = transactionsGet.get_json()
    assert productsJson[0]["id"] == 1
    assert productsJson[0]["name"] == "Product"
    assert productsJson[0]["quantity_on_hand"] == 2
    assert productsJson[0]["reorder_level"] == 1
    assert productsJson[0]["sku"] == "A"
    assert productsJson[0]["unit_price"] == 1

# TEST 4D: Two Products Alternative Case (Lines 53-54, 56-67)
def test_suppliers_two_products_alternative_case_lines_53_to_54_and_56_to_67(client):
    productsPost1 = client.post("/products", json = {"name": "Product 1", "quantity_on_hand": 1, "reorder_level": 1, "sku": "A", "unit_price": 1})
    assert productsPost1.status_code == 201
    
    productJson1 = productsPost1.get_json()
    assert productJson1["id"] == 1
    assert productJson1["name"] == "Product 1"
    assert productJson1["quantity_on_hand"] == 1
    assert productJson1["reorder_level"] == 1
    assert productJson1["sku"] == "A"
    assert productJson1["unit_price"] == 1 

    productsPost2 = client.post("/products", json = {"name": "Product 2", "quantity_on_hand": 2, "reorder_level": 2, "sku": "B", "unit_price": 2})
    assert productsPost2.status_code == 201

    productJson2 = productsPost2.get_json()
    assert productJson2["id"] == 2
    assert productJson2["name"] == "Product 2"
    assert productJson2["quantity_on_hand"] == 2
    assert productJson2["reorder_level"] == 2
    assert productJson2["sku"] == "B"
    assert productJson2["unit_price"] == 2

    suppliersPost = client.post("/suppliers", json = {"contact_email": "johndoe@email.com", "name": "Supplier"})
    assert suppliersPost.status_code == 201
        
    supplierJSON = suppliersPost.get_json()
    assert supplierJSON["contact_email"] == "johndoe@email.com"
    assert supplierJSON["id"] == 1
    assert supplierJSON["name"] == "Supplier"

    transactionsPost1 = client.post("/transactions", json = {"product_id": 1, "quantity": 1, "supplier_id": 1, "type": "IN"})
    assert transactionsPost1.status_code == 201
    
    transactionJSON1 = transactionsPost1.get_json()
    transactionJSON1["product_id"] == 1
    transactionJSON1["quantity"] == 1
    transactionJSON1["supplier_id"] == 1
    transactionJSON1["transaction_date"] == date.today().isoformat()
    transactionJSON1["type"] == "IN"

    transactionsPost2 = client.post("/transactions", json = {"product_id": 2, "quantity": 2, "supplier_id": 1, "type": "IN"})
    assert transactionsPost2.status_code == 201
        
    transactionJSON2 = transactionsPost2.get_json()
    transactionJSON2["product_id"] == 2
    transactionJSON2["quantity"] == 2
    transactionJSON2["supplier_id"] == 2
    transactionJSON2["transaction_date"] == date.today().isoformat()
    transactionJSON2["type"] == "IN"

    transactionsGet = client.get("/suppliers/1/products")
    assert transactionsGet.status_code == 200

    productsJson = transactionsGet.get_json()
    assert productsJson[0]["id"] == 1
    assert productsJson[0]["name"] == "Product 1"
    assert productsJson[0]["quantity_on_hand"] == 2
    assert productsJson[0]["reorder_level"] == 1
    assert productsJson[0]["sku"] == "A"
    assert productsJson[0]["unit_price"] == 1
    assert productsJson[1]["id"] == 2
    assert productsJson[1]["name"] == "Product 2"
    assert productsJson[1]["quantity_on_hand"] == 4
    assert productsJson[1]["reorder_level"] == 2
    assert productsJson[1]["sku"] == "B"
    assert productsJson[1]["unit_price"] == 2

# TEST 4E: No Products Alternative Case (Lines 53-54, 56-67)
def test_suppliers_no_products_alternative_case_lines_53_to_54_and_56_to_67(client):
    productsPost = client.post("/products", json = {"name": "Product", "quantity_on_hand": 1, "reorder_level": 1, "sku": "A", "unit_price": 1})
    assert productsPost.status_code == 201
        
    productJson = productsPost.get_json()
    assert productJson["id"] == 1
    assert productJson["name"] == "Product"
    assert productJson["quantity_on_hand"] == 1
    assert productJson["reorder_level"] == 1
    assert productJson["sku"] == "A"
    assert productJson["unit_price"] == 1
    
    suppliersPost = client.post("/suppliers", json = {"contact_email": "johndoe@email.com", "name": "Supplier"})
    assert suppliersPost.status_code == 201
    
    supplierJSON = suppliersPost.get_json()
    assert supplierJSON["contact_email"] == "johndoe@email.com"
    assert supplierJSON["id"] == 1
    assert supplierJSON["name"] == "Supplier"
            
    transactionsPost = client.post("/transactions", json = {"product_id": 1, "quantity": 1, "supplier_id": 1, "type": "OUT"})
    assert transactionsPost.status_code == 201
        
    transactionJSON = transactionsPost.get_json()
    transactionJSON["product_id"] == 1
    transactionJSON["quantity"] == 1
    transactionJSON["supplier_id"] == 1
    transactionJSON["transaction_date"] == date.today().isoformat()
    transactionJSON["type"] == "OUT"
    
    transactionsGet = client.get("/suppliers/1/products")
    assert transactionsGet.status_code == 200
    
    productsJson = transactionsGet.get_json()
    assert productsJson == list()

# TEST 4F: Empty Supplier Failure Case (Line 55)
def test_suppliers_empty_supplier_failure_case_line_55(client):
    transactionGet = client.get("/suppliers/1/products")
    assert transactionGet.status_code == 404

    productsJson = transactionGet.get_json()
    assert productsJson["error"] == "Supplier not found"

# TEST 5: app/routes/transactions.py

# TEST 5A: Empty Product Transaction Create Failure Case (Line 26)
def test_transactions_empty_product_transaction_create_failure_case_line_26(client):    
    transactionsPost = client.post("/transactions", json = {"product_id": 1, "quantity": 1, "type": "IN"})
    assert transactionsPost.status_code == 404

    createJson = transactionsPost.get_json()
    createJson["error"] == "Product not found"

# TEST 5B: OUT Transaction Type Alternative Case (Lines 33-34)
def test_transactions_OUT_transaction_type_alternative_case_lines_33_to_34(client):
    productsPost = client.post("/products", json = {"name": "Product", "quantity_on_hand": 1, "reorder_level": 1, "sku": "A", "unit_price": 1})
    assert productsPost.status_code == 201

    productJson = productsPost.get_json()
    assert productJson["id"] == 1
    assert productJson["name"] == "Product"
    assert productJson["quantity_on_hand"] == 1
    assert productJson["reorder_level"] == 1
    assert productJson["sku"] == "A"
    assert productJson["unit_price"] == 1
    
    transactionsPost = client.post("/transactions", json = {"product_id": 1, "quantity": 1, "type": "OUT"})
    assert transactionsPost.status_code == 201

    transactionJSON = transactionsPost.get_json()
    transactionJSON["product_id"] == 1
    transactionJSON["quantity"] == 1
    transactionJSON["supplier_id"] == None
    transactionJSON["transaction_date"] == date.today().isoformat()
    transactionJSON["type"] == "OUT"

# TEST 5C: Invalid Transaction Type Failure Case (Line 36)
def test_transactions_invalid_transaction_type_failure_case_line_36(client):
    productsPost = client.post("/products", json = {"name": "Product", "quantity_on_hand": 1, "reorder_level": 1, "sku": "A", "unit_price": 1})
    assert productsPost.status_code == 201

    productJson = productsPost.get_json()
    assert productJson["id"] == 1
    assert productJson["name"] == "Product"
    assert productJson["quantity_on_hand"] == 1
    assert productJson["reorder_level"] == 1
    assert productJson["sku"] == "A"
    assert productJson["unit_price"] == 1

    transactionsPost = client.post("/transactions", json = {"product_id": 1, "quantity": 1, "type": "BETWEEN"})
    assert transactionsPost.status_code == 400

    transactionJSON = transactionsPost.get_json()
    assert transactionJSON["error"] == "type must be IN or OUT"
