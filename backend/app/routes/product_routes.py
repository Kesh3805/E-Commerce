from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.product import Product
from app.utils.security import admin_required, validate_required_fields
import json

product_bp = Blueprint("products", __name__)


@product_bp.route("", methods=["GET"])
def get_products():
    """Get all products with search, filter, sort, pagination."""
    search = request.args.get("search", "").strip()
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    category_id = request.args.get("category_id", type=int)
    brand = request.args.get("brand", "").strip()
    featured = request.args.get("featured", "").lower()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 12, type=int)

    query = Product.query.filter_by(is_active=True)

    if search:
        query = query.filter(
            db.or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%"),
                Product.brand.ilike(f"%{search}%"),
            )
        )
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if brand:
        query = query.filter(Product.brand.ilike(f"%{brand}%"))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if featured == "true":
        query = query.filter(Product.is_featured == True)

    # Sort options
    sort = request.args.get("sort", "newest")
    if sort == "price_low":
        query = query.order_by(Product.price.asc())
    elif sort == "price_high":
        query = query.order_by(Product.price.desc())
    elif sort == "name":
        query = query.order_by(Product.name.asc())
    elif sort == "popular":
        query = query.order_by(Product.is_featured.desc(), Product.created_at.desc())
    else:
        query = query.order_by(Product.created_at.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "products": [p.to_dict() for p in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page,
    }), 200


@product_bp.route("/featured", methods=["GET"])
def get_featured_products():
    """Get featured products for homepage."""
    limit = request.args.get("limit", 8, type=int)
    products = Product.query.filter_by(is_featured=True, is_active=True)\
        .order_by(Product.created_at.desc()).limit(limit).all()
    return jsonify({"products": [p.to_dict() for p in products]}), 200


@product_bp.route("/deals", methods=["GET"])
def get_deals():
    """Get products with discounts."""
    limit = request.args.get("limit", 8, type=int)
    products = Product.query.filter(
        Product.compare_price.isnot(None),
        Product.compare_price > Product.price,
        Product.is_active == True,
    ).order_by(Product.created_at.desc()).limit(limit).all()
    return jsonify({"products": [p.to_dict() for p in products]}), 200


@product_bp.route("/brands", methods=["GET"])
def get_brands():
    """Get all distinct brands."""
    brands = db.session.query(Product.brand)\
        .filter(Product.brand.isnot(None), Product.brand != "", Product.is_active == True)\
        .distinct().order_by(Product.brand).all()
    return jsonify({"brands": [b[0] for b in brands]}), 200


@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Get a single product by ID."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"product": product.to_dict()}), 200


@product_bp.route("", methods=["POST"])
@jwt_required()
@admin_required
def create_product():
    """Create a new product (Admin only)."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    valid, msg = validate_required_fields(data, ["name", "price"])
    if not valid:
        return jsonify({"error": msg}), 400

    # Validate price and stock
    try:
        price = float(data["price"])
        if price <= 0:
            return jsonify({"error": "Price must be greater than 0"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid price format"}), 400

    try:
        stock = int(data.get("stock", 0))
        if stock < 0:
            return jsonify({"error": "Stock cannot be negative"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid stock format"}), 400

    product = Product(
        name=data["name"].strip(),
        description=data.get("description", ""),
        price=price,
        compare_price=float(data["compare_price"]) if data.get("compare_price") else None,
        stock=stock,
        image_url=data.get("image_url", ""),
        images=json.dumps(data.get("images", [])),
        brand=data.get("brand", ""),
        sku=data.get("sku"),
        is_featured=data.get("is_featured", False),
        is_active=data.get("is_active", True),
        category_id=data.get("category_id"),
    )
    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product created", "product": product.to_dict()}), 201


@product_bp.route("/<int:product_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_product(product_id):
    """Update a product (Admin only)."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if "name" in data:
        product.name = data["name"].strip()
    if "description" in data:
        product.description = data["description"]
    if "price" in data:
        product.price = float(data["price"])
    if "compare_price" in data:
        product.compare_price = float(data["compare_price"]) if data["compare_price"] else None
    if "stock" in data:
        product.stock = int(data["stock"])
    if "image_url" in data:
        product.image_url = data["image_url"]
    if "images" in data:
        product.images = json.dumps(data["images"])
    if "brand" in data:
        product.brand = data["brand"]
    if "sku" in data:
        product.sku = data["sku"]
    if "is_featured" in data:
        product.is_featured = data["is_featured"]
    if "is_active" in data:
        product.is_active = data["is_active"]
    if "category_id" in data:
        product.category_id = data["category_id"]

    db.session.commit()
    return jsonify({"message": "Product updated", "product": product.to_dict()}), 200


@product_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_product(product_id):
    """Delete a product (Admin only)."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200
