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
