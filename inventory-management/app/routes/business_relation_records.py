from datetime import date
from flask import Blueprint, jsonify, request

from app import store
from app.models.business_relation_record import Business_Relation_Record

business_relation_records_bp = Blueprint("business_relation_records", __name__, url_prefix="/business_relation_records")

@business_relation_records_bp.route("", methods=["GET"])
def list_business_relation_records():
    return jsonify([p.to_dict() for p in store.business_relation_records.values()])

@business_relation_records_bp.route("/<int:record_id>", methods=["GET"])
def get_purchase_order(record_id):
    record = store.purchase_orders.get(record_id)
    if record is None:
        return jsonify({"error": "Record not found"}), 404
    return jsonify(record.to_dict())

@business_relation_records_bp.route("", methods=["POST"])
def create_business_relation_record():
    data = request.get_json()

    po_id = store.next_id("business_relation_record")
    po = Business_Relation_Record(
        id=po_id,
        supplier_id=data["supplier_id"],
        quantity_deliveries=data["quantity_deliveries"],
        creation_date=data["creation_date"],
        update_date=date.today().isoformat(),
    )
    store.business_relation_records[po_id] = po
    return jsonify(po.to_dict()), 201

@business_relation_records_bp.route("/<int:record_id>", methods=["DELETE"])
def delete_business_relation_record(record_id):
    business_relation_record = store.business_relation_records.pop(record_id, None)
    if business_relation_record is None:
        return jsonify({"error": "Record not found"}), 404
    return "", 204