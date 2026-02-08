from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.coupon import Coupon
from app.utils.security import admin_required

coupon_bp = Blueprint("coupons", __name__)


@coupon_bp.route("/validate", methods=["POST"])
@jwt_required()
def validate_coupon():
    """Validate a coupon code and return discount info."""
    data = request.get_json()
    if not data or "code" not in data:
        return jsonify({"error": "Coupon code is required"}), 400

    coupon = Coupon.query.filter_by(code=data["code"].upper()).first()
    if not coupon:
        return jsonify({"error": "Invalid coupon code"}), 404
    if not coupon.is_valid:
        return jsonify({"error": "This coupon has expired or is no longer valid"}), 400

    order_total = data.get("order_total", 0)
    discount = coupon.calculate_discount(order_total)

    return jsonify({
        "valid": True,
        "coupon": coupon.to_dict(),
        "discount": discount,
        "final_total": max(0, order_total - discount),
    }), 200


@coupon_bp.route("", methods=["GET"])
@jwt_required()
@admin_required
def get_coupons():
    """Get all coupons (Admin only)."""
    coupons = Coupon.query.order_by(Coupon.created_at.desc()).all()
    return jsonify({"coupons": [c.to_dict() for c in coupons]}), 200


@coupon_bp.route("", methods=["POST"])
@jwt_required()
@admin_required
def create_coupon():
    """Create a new coupon (Admin only)."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required = ["code", "discount_type", "discount_value"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    code = data["code"].upper().strip()
    if Coupon.query.filter_by(code=code).first():
        return jsonify({"error": "Coupon code already exists"}), 400

    from datetime import datetime
    expires_at = None
    if data.get("expires_at"):
        try:
            expires_at = datetime.fromisoformat(data["expires_at"])
        except ValueError:
            return jsonify({"error": "Invalid date format for expires_at"}), 400

    coupon = Coupon(
        code=code,
        discount_type=data["discount_type"],
        discount_value=float(data["discount_value"]),
        min_order_amount=float(data.get("min_order_amount", 0)),
        max_discount=float(data.get("max_discount", 0)) if data.get("max_discount") else None,
        usage_limit=int(data.get("usage_limit", 0)) if data.get("usage_limit") else None,
        expires_at=expires_at,
    )
    db.session.add(coupon)
    db.session.commit()

    return jsonify({"message": "Coupon created", "coupon": coupon.to_dict()}), 201


@coupon_bp.route("/<int:coupon_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_coupon(coupon_id):
    """Delete a coupon (Admin only)."""
    coupon = Coupon.query.get(coupon_id)
    if not coupon:
        return jsonify({"error": "Coupon not found"}), 404

    db.session.delete(coupon)
    db.session.commit()
    return jsonify({"message": "Coupon deleted"}), 200
