from flask import Blueprint, jsonify, request

from app import store
from app.models.product import Product

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
@products_bp.route("/<int:product_id>/is-below-reorder-level", methods=["POST"])
def invoke_alert(product_id):
    product = store.products.get(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    if not product.is_below_reorder_level and product.quantity_on_hand <= product.reorder_level / 2:
        product.is_below_reorder_level = True
        return jsonify({"message": f"Stock alert for {product.name} ({product.id}): {product.reorder_level - product.quantity_on_hand} more are needed to restore target levels."}), 200
# Functional enhancement end
