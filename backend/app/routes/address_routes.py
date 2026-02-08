from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.address import Address

address_bp = Blueprint("addresses", __name__)


@address_bp.route("", methods=["GET"])
@jwt_required()
def get_addresses():
    """Get all addresses for current user."""
    user_id = int(get_jwt_identity())
    addresses = Address.query.filter_by(user_id=user_id).order_by(Address.is_default.desc()).all()
    return jsonify({"addresses": [a.to_dict() for a in addresses]}), 200


@address_bp.route("", methods=["POST"])
@jwt_required()
def add_address():
    """Add a new address."""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required = ["full_name", "phone", "address_line1", "city", "state", "zip_code"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    # If this is the first address or marked as default, unset others
    is_default = data.get("is_default", False)
    if is_default or Address.query.filter_by(user_id=user_id).count() == 0:
        Address.query.filter_by(user_id=user_id).update({"is_default": False})
        is_default = True

    address = Address(
        user_id=user_id,
        label=data.get("label", "Home"),
        full_name=data["full_name"],
        phone=data["phone"],
        address_line1=data["address_line1"],
        address_line2=data.get("address_line2", ""),
        city=data["city"],
        state=data["state"],
        zip_code=data["zip_code"],
        country=data.get("country", "US"),
        is_default=is_default,
    )
    db.session.add(address)
    db.session.commit()

    return jsonify({"message": "Address added", "address": address.to_dict()}), 201


@address_bp.route("/<int:address_id>", methods=["PUT"])
@jwt_required()
def update_address(address_id):
    """Update an address."""
    user_id = int(get_jwt_identity())
    address = Address.query.filter_by(id=address_id, user_id=user_id).first()
    if not address:
        return jsonify({"error": "Address not found"}), 404

    data = request.get_json()
    for field in ["label", "full_name", "phone", "address_line1", "address_line2",
                   "city", "state", "zip_code", "country"]:
        if field in data:
            setattr(address, field, data[field])

    if data.get("is_default"):
        Address.query.filter_by(user_id=user_id).update({"is_default": False})
        address.is_default = True

    db.session.commit()
    return jsonify({"message": "Address updated", "address": address.to_dict()}), 200


@address_bp.route("/<int:address_id>", methods=["DELETE"])
@jwt_required()
def delete_address(address_id):
    """Delete an address."""
    user_id = int(get_jwt_identity())
    address = Address.query.filter_by(id=address_id, user_id=user_id).first()
    if not address:
        return jsonify({"error": "Address not found"}), 404

    was_default = address.is_default
    db.session.delete(address)

    # If deleted was default, make another one default
    if was_default:
        first = Address.query.filter_by(user_id=user_id).first()
        if first:
            first.is_default = True

    db.session.commit()
    return jsonify({"message": "Address deleted"}), 200


@address_bp.route("/<int:address_id>/default", methods=["PUT"])
@jwt_required()
def set_default_address(address_id):
    """Set an address as default."""
    user_id = int(get_jwt_identity())
    address = Address.query.filter_by(id=address_id, user_id=user_id).first()
    if not address:
        return jsonify({"error": "Address not found"}), 404

    Address.query.filter_by(user_id=user_id).update({"is_default": False})
    address.is_default = True
    db.session.commit()

    return jsonify({"message": "Default address updated"}), 200
