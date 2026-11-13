from datetime import date
from app.models.purchase_order import PurchaseOrder

# TEST 1: app/models/purchase_order.py

# TEST 1A: Trivial Case
def test_purchase_order_trivial_case():
    purchaseOrder = PurchaseOrder(id = 1, supplier_id = 1, product_id = 1, quantity_ordered = 1)   
    dictionary = purchaseOrder.to_dict()
    assert dictionary["id"] == 1
    assert dictionary["supplier_id"] == 1
    assert dictionary["product_id"] == 1
    assert dictionary["quantity_ordered"] == 1
    assert dictionary["status"] == "pending"
    assert dictionary["created_date"] == date.today().isoformat()
    assert dictionary["received_date"] == None

# TEST 1B: Non-Empty received_date Alternative Case
def test_purchase_order_nonempty_received_date_alternative_case():
    purchaseOrder = PurchaseOrder(id = 1, supplier_id = 1, product_id = 1, quantity_ordered = 1, received_date = date.today())   
    dictionary = purchaseOrder.to_dict()
    assert dictionary["id"] == 1
    assert dictionary["supplier_id"] == 1
    assert dictionary["product_id"] == 1
    assert dictionary["quantity_ordered"] == 1
    assert dictionary["status"] == "pending"
    assert dictionary["created_date"] == date.today().isoformat()
    assert dictionary["received_date"] == date.today().isoformat()

# TEST 1C: Empty Arguments Failure Case
def test_purchase_order_empty_arguments_failure_case():
    try:
        PurchaseOrder()
    except:
        assert True
        return
    assert False
