from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.order_service import OrderService
from app.utils.security import admin_required
from app.models.user import User
from app.models.order import Order
from app.extensions import db

order_bp = Blueprint("orders", __name__)


@order_bp.route("/place", methods=["POST"])
@jwt_required()
def place_order():
    """Place an order from the current cart."""
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    order, error = OrderService.place_order(
        user_id,
        address_id=data.get("address_id"),
        coupon_code=data.get("coupon_code"),
        payment_method=data.get("payment_method", "COD"),
    )
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Order placed successfully", "order": order.to_dict()}), 201


@order_bp.route("", methods=["GET"])
@jwt_required()
def get_orders():
    """Get orders — user sees own orders, admin sees all."""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if user and user.role == "ADMIN":
        from app.models.order import Order
        orders = Order.query.order_by(Order.created_at.desc()).all()
    else:
        orders = OrderService.get_user_orders(user_id)

    return jsonify({"orders": [o.to_dict() for o in orders]}), 200


@order_bp.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order(order_id):
    """Get a single order by ID."""
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    is_admin = user and user.role == "ADMIN"

    order, error = OrderService.get_order_by_id(order_id, user_id=user_id, is_admin=is_admin)
    if error:
        return jsonify({"error": error}), 404
    return jsonify({"order": order.to_dict()}), 200


@order_bp.route("/<int:order_id>/status", methods=["PUT"])
@jwt_required()
@admin_required
def update_order_status(order_id):
    """Update order status (Admin only)."""
    data = request.get_json()
    if not data or "status" not in data:
        return jsonify({"error": "Status is required"}), 400

    order, error = OrderService.update_status(order_id, data["status"])
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Order status updated", "order": order.to_dict()}), 200


@order_bp.route("/stats", methods=["GET"])
@jwt_required()
@admin_required
def get_order_stats():
    """Get order statistics (Admin only)."""
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_price)).scalar() or 0
    
    status_counts = db.session.query(
        Order.status, db.func.count(Order.id)
    ).group_by(Order.status).all()
    
    status_breakdown = {status: count for status, count in status_counts}
    
    # Recent orders (last 10)
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    return jsonify({
        "total_orders": total_orders,
        "total_revenue": round(total_revenue, 2),
        "status_breakdown": status_breakdown,
        "recent_orders": [o.to_dict() for o in recent_orders]
    }), 200
