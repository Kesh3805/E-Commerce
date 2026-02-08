from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.cart import Cart
from app.models.product import Product
from app.utils.security import validate_required_fields

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("", methods=["GET"])
@jwt_required()
def get_cart():
    """Get current user's cart."""
    user_id = int(get_jwt_identity())
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    total = sum(item.product.price * item.quantity for item in cart_items if item.product)

    return jsonify({
        "cart": [item.to_dict() for item in cart_items],
        "total": round(total, 2),
        "item_count": len(cart_items),
    }), 200


@cart_bp.route("/add", methods=["POST"])
@jwt_required()
def add_to_cart():
    """Add a product to cart."""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    valid, msg = validate_required_fields(data, ["product_id"])
    if not valid:
        return jsonify({"error": msg}), 400

    product_id = int(data["product_id"])
    quantity = int(data.get("quantity", 1))

    if quantity < 1:
        return jsonify({"error": "Quantity must be at least 1"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    if not product.is_available:
        return jsonify({"error": "Product is out of stock"}), 400
    
    if product.stock < quantity:
        return jsonify({
            "error": f"Insufficient stock. Only {product.stock} available"
        }), 400

    # Check if item already in cart
    existing = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing:
        new_quantity = existing.quantity + quantity
        if product.stock < new_quantity:
            return jsonify({
                "error": f"Cannot add more. Only {product.stock} available (you have {existing.quantity} in cart)"
            }), 400
        existing.quantity = new_quantity
    else:
        cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({"message": "Product added to cart"}), 200


@cart_bp.route("/update", methods=["PUT"])
@jwt_required()
def update_cart():
    """Update cart item quantity."""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    valid, msg = validate_required_fields(data, ["product_id", "quantity"])
    if not valid:
        return jsonify({"error": msg}), 400

    product_id = int(data["product_id"])
    quantity = int(data["quantity"])

    if quantity < 1:
        return jsonify({"error": "Quantity must be at least 1"}), 400

    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not cart_item:
        return jsonify({"error": "Item not in cart"}), 404

    product = Product.query.get(product_id)
    if product and product.stock < quantity:
        return jsonify({"error": "Insufficient stock"}), 400

    cart_item.quantity = quantity
    db.session.commit()

    return jsonify({"message": "Cart updated"}), 200


@cart_bp.route("/remove/<int:product_id>", methods=["DELETE"])
@jwt_required()
def remove_from_cart(product_id):
    """Remove an item from cart."""
    user_id = int(get_jwt_identity())

    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not cart_item:
        return jsonify({"error": "Item not in cart"}), 404

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({"message": "Item removed from cart"}), 200
