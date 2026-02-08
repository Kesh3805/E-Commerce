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
    
    if not coupon.is_active:
        return jsonify({"error": "This coupon is no longer active"}), 400
    
    if coupon.usage_limit and coupon.times_used >= coupon.usage_limit:
        return jsonify({"error": "This coupon has reached its usage limit"}), 400
    
    if coupon.expires_at:
        from datetime import datetime, timezone
        if datetime.now(timezone.utc) > coupon.expires_at:
            return jsonify({"error": "This coupon has expired"}), 400

    order_total = data.get("order_total", 0)
    
    if order_total < coupon.min_order_amount:
        return jsonify({
            "error": f"Minimum order amount of ${coupon.min_order_amount:.2f} required to use this coupon"
        }), 400
    
    discount = coupon.calculate_discount(order_total)

    return jsonify({
        "valid": True,
        "coupon": coupon.to_dict(),
        "discount": discount,
        "final_total": max(0, order_total - discount),
    }), 200


@coupon_bp.route("", methods=["GET"])
@jwt_required()
def get_coupons():
    """Get coupons - users see active coupons, admin sees all."""
    from flask_jwt_extended import get_jwt_identity
    from app.models.user import User
    
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if user and user.role == "ADMIN":
        # Admin sees all coupons
        coupons = Coupon.query.order_by(Coupon.created_at.desc()).all()
    else:
        # Regular users see only active, valid coupons
        from datetime import datetime, timezone
        coupons = Coupon.query.filter(
            Coupon.is_active == True,
            db.or_(
                Coupon.expires_at == None,
                Coupon.expires_at > datetime.now(timezone.utc)
            )
        ).all()
        # Filter out usage limit reached coupons
        coupons = [c for c in coupons if not (c.usage_limit and c.times_used >= c.usage_limit)]
    
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
