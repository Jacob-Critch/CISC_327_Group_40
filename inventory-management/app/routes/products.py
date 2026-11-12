from flask import Blueprint, jsonify, request

from app import store
from app.models.product import Product

from notification_service import *

products_bp = Blueprint("products", __name__, url_prefix="/products")


@products_bp.route("", methods=["GET"])
def list_products():
    return jsonify([p.to_dict() for p in store.products.values()])


@products_bp.route("/low-stock", methods=["GET"])
def low_stock():
    """Return products where quantity_on_hand is at or below their reorder_level."""
    flagged = [
        p for p in store.products.values()
        if p.quantity_on_hand <= p.reorder_level
    ]
    return jsonify([p.to_dict() for p in flagged])


@products_bp.route("", methods=["POST"])
def create_product():
    data = request.get_json()
    product_id = store.next_id("product")
    product = Product(
        id=product_id,
        name=data["name"],
        sku=data["sku"],
        unit_price=data.get("unit_price", 0.0),
        quantity_on_hand=data.get("quantity_on_hand", 0),
        reorder_level=data.get("reorder_level", 0),
    )
    store.products[product_id] = product
    return jsonify(product.to_dict()), 201


@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = store.products.get(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict())


@products_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = store.products.get(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    data = request.get_json()
    product.name = data.get("name", product.name)
    product.sku = data.get("sku", product.sku)
    product.unit_price = data.get("unit_price", product.unit_price)
    product.quantity_on_hand = data.get("quantity_on_hand", product.quantity_on_hand)
    product.reorder_level = data.get("reorder_level", product.reorder_level)
    return jsonify(product.to_dict())


@products_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = store.products.pop(product_id, None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return "", 204

@products_bp.route("/<int:product_id>/stock-level", methods=["GET"])
def stock_level(product_id):
    product = store.products.get(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"product_id": product.id, "quantity_on_hand": product.quantity_on_hand})

# Functional enhancement beginning
@products_bp.route("/send-stock-alert/<int:product_id>", methods=["POST"])
def send_stock_alert(product_id):
    if not is_service_available():
        return jsonify({"error": "Notification service is offline."}), 404

    product = store.products.get(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    message = f"Stock alert for {product.name} ({product.id}): {product.reorder_level - product.quantity_on_hand} more are needed to restore target levels."
    for admin in store.ADMIN_EMAILS:
        sent = send_notification(admin, "Stock alert", message)
        if not sent:
            return jsonify({"error": f"Failed to send a stock alert to admin {admin}."}), 404
    return jsonify({"message": f"Sent a stock alert to admins."}), 200

@products_bp.route("/<int:product_id>/is-below-reorder-level", methods=["POST"])
def invoke_alert(product_id):
    product = store.products.get(product_id)

    if product is None:
        return jsonify({"error": "Product not found"}), 404
    
    if product.quantity_on_hand <= product.reorder_level / 2:
        if not product.is_below_reorder_level:
            product.is_below_reorder_level = True

            message = f"Stock alert for {product.name} ({product.id}): {product.reorder_level - product.quantity_on_hand} more are needed to restore target levels."
            
            return jsonify({"message": message}), 200
    else:
        product.is_below_reorder_level = False
    return jsonify({"message": f"No stock alert for {product.name} ({product.id})."}), 200
# Functional enhancement end
