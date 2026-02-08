from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.category import Category
from app.utils.security import admin_required

category_bp = Blueprint("categories", __name__)


@category_bp.route("", methods=["GET"])
def get_categories():
    """Get all top-level categories with children."""
    categories = Category.query.filter_by(parent_id=None).order_by(Category.name).all()
    return jsonify({
        "categories": [c.to_dict(include_children=True) for c in categories]
    }), 200


@category_bp.route("/<int:category_id>", methods=["GET"])
def get_category(category_id):
    """Get single category with products."""
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 12, type=int)
    sort = request.args.get("sort", "newest")

    from app.models.product import Product
    query = Product.query.filter_by(category_id=category_id, is_active=True)

    if sort == "price_low":
        query = query.order_by(Product.price.asc())
    elif sort == "price_high":
        query = query.order_by(Product.price.desc())
    elif sort == "name":
        query = query.order_by(Product.name.asc())
    else:
        query = query.order_by(Product.created_at.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "category": category.to_dict(include_children=True),
        "products": [p.to_dict() for p in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page,
    }), 200


@category_bp.route("/slug/<slug>", methods=["GET"])
def get_category_by_slug(slug):
    """Get category by slug."""
    category = Category.query.filter_by(slug=slug).first()
    if not category:
        return jsonify({"error": "Category not found"}), 404
    return jsonify({"category": category.to_dict(include_children=True)}), 200


@category_bp.route("", methods=["POST"])
@jwt_required()
@admin_required
def create_category():
    """Create a category (Admin only)."""
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    name = data["name"].strip()
    slug = data.get("slug", name.lower().replace(" ", "-").replace("&", "and"))

    if Category.query.filter_by(slug=slug).first():
        return jsonify({"error": "Category with this slug already exists"}), 400

    category = Category(
        name=name,
        slug=slug,
        description=data.get("description", ""),
        image_url=data.get("image_url", ""),
        parent_id=data.get("parent_id"),
    )
    db.session.add(category)
    db.session.commit()

    return jsonify({"message": "Category created", "category": category.to_dict()}), 201


@category_bp.route("/<int:category_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_category(category_id):
    """Update a category (Admin only)."""
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    data = request.get_json()
    if "name" in data:
        category.name = data["name"].strip()
    if "slug" in data:
        category.slug = data["slug"]
    if "description" in data:
        category.description = data["description"]
    if "image_url" in data:
        category.image_url = data["image_url"]
    if "parent_id" in data:
        category.parent_id = data["parent_id"]

    db.session.commit()
    return jsonify({"message": "Category updated", "category": category.to_dict()}), 200


@category_bp.route("/<int:category_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_category(category_id):
    """Delete a category (Admin only)."""
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200
