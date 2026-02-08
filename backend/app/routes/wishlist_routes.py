from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.wishlist import Wishlist
from app.models.product import Product

wishlist_bp = Blueprint("wishlist", __name__)


@wishlist_bp.route("", methods=["GET"])
@jwt_required()
def get_wishlist():
    """Get current user's wishlist."""
    user_id = int(get_jwt_identity())
    items = Wishlist.query.filter_by(user_id=user_id).order_by(Wishlist.created_at.desc()).all()

    return jsonify({
        "wishlist": [item.to_dict() for item in items],
        "count": len(items),
    }), 200


@wishlist_bp.route("/add", methods=["POST"])
@jwt_required()
def add_to_wishlist():
    """Add a product to wishlist."""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data or "product_id" not in data:
        return jsonify({"error": "product_id is required"}), 400

    product_id = int(data["product_id"])
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    existing = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing:
        return jsonify({"error": "Product already in wishlist"}), 400

    item = Wishlist(user_id=user_id, product_id=product_id)
    db.session.add(item)
    db.session.commit()

    return jsonify({"message": "Added to wishlist"}), 201


@wishlist_bp.route("/remove/<int:product_id>", methods=["DELETE"])
@jwt_required()
def remove_from_wishlist(product_id):
    """Remove a product from wishlist."""
    user_id = int(get_jwt_identity())
    item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not item:
        return jsonify({"error": "Product not in wishlist"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Removed from wishlist"}), 200


@wishlist_bp.route("/check/<int:product_id>", methods=["GET"])
@jwt_required()
def check_wishlist(product_id):
    """Check if a product is in the user's wishlist."""
    user_id = int(get_jwt_identity())
    exists = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first() is not None
    return jsonify({"in_wishlist": exists}), 200


@wishlist_bp.route("/move-to-cart/<int:product_id>", methods=["POST"])
@jwt_required()
def move_to_cart(product_id):
    """Move a product from wishlist to cart."""
    user_id = int(get_jwt_identity())

    wishlist_item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not wishlist_item:
        return jsonify({"error": "Product not in wishlist"}), 404

    product = Product.query.get(product_id)
    if not product or not product.is_available:
        return jsonify({"error": "Product is not available"}), 400

    from app.models.cart import Cart
    existing_cart = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing_cart:
        existing_cart.quantity += 1
    else:
        cart_item = Cart(user_id=user_id, product_id=product_id, quantity=1)
        db.session.add(cart_item)

    db.session.delete(wishlist_item)
    db.session.commit()

    return jsonify({"message": "Moved to cart"}), 200
