from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService
from app.utils.security import validate_required_fields

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    valid, msg = validate_required_fields(data, ["name", "email", "password"])
    if not valid:
        return jsonify({"error": msg}), 400

    user, error = AuthService.register(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        role=data.get("role", "USER"),
    )
    if error:
        return jsonify({"error": error}), 400

    return jsonify({"message": "Registration successful", "user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    valid, msg = validate_required_fields(data, ["email", "password"])
    if not valid:
        return jsonify({"error": msg}), 400

    access_token, refresh_token, error = AuthService.login(
        email=data["email"],
        password=data["password"],
    )
    if error:
        return jsonify({"error": error}), 401

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
    }), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user, error = AuthService.get_profile(int(user_id))
    if error:
        return jsonify({"error": error}), 404

    return jsonify({"user": user.to_dict()}), 200


@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    """Update user profile."""
    user_id = int(get_jwt_identity())
    from app.models.user import User
    from app.extensions import db

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if "name" in data:
        user.name = data["name"].strip()
    if "phone" in data:
        user.phone = data["phone"]
    if "avatar" in data:
        user.avatar = data["avatar"]

    db.session.commit()
    return jsonify({"message": "Profile updated", "user": user.to_dict()}), 200
