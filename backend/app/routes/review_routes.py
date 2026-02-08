from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.review import Review
from app.models.product import Product
from app.models.order import Order, OrderItem

review_bp = Blueprint("reviews", __name__)


@review_bp.route("/product/<int:product_id>", methods=["GET"])
def get_product_reviews(product_id):
    """Get all reviews for a product."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    sort = request.args.get("sort", "newest")

    query = Review.query.filter_by(product_id=product_id)

    if sort == "highest":
        query = query.order_by(Review.rating.desc())
    elif sort == "lowest":
        query = query.order_by(Review.rating.asc())
    else:
        query = query.order_by(Review.created_at.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Calculate rating distribution
    from sqlalchemy import func
    distribution = db.session.query(
        Review.rating, func.count(Review.id)
    ).filter_by(product_id=product_id).group_by(Review.rating).all()
    rating_dist = {str(i): 0 for i in range(1, 6)}
    for rating, count in distribution:
        rating_dist[str(rating)] = count

    total_reviews = sum(rating_dist.values())
    avg = db.session.query(func.avg(Review.rating)).filter_by(product_id=product_id).scalar()

    return jsonify({
        "reviews": [r.to_dict() for r in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page,
        "avg_rating": round(float(avg), 1) if avg else 0,
        "total_reviews": total_reviews,
        "rating_distribution": rating_dist,
    }), 200


@review_bp.route("", methods=["POST"])
@jwt_required()
def create_review():
    """Create a review for a product (must have purchased it)."""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    product_id = data.get("product_id")
    rating = data.get("rating")
    if not product_id or not rating:
        return jsonify({"error": "product_id and rating are required"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Check if user already reviewed
    existing = Review.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing:
        return jsonify({"error": "You have already reviewed this product"}), 400

    # Validate rating
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return jsonify({"error": "Rating must be between 1 and 5"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid rating"}), 400

    # Check if user has purchased this product
    has_purchased = db.session.query(OrderItem).join(Order).filter(
        Order.user_id == user_id,
        OrderItem.product_id == product_id,
        Order.status.in_(["PLACED", "SHIPPED", "DELIVERED"])
    ).first()

    if not has_purchased:
        return jsonify({"error": "You can only review products you have purchased"}), 403

    review = Review(
        user_id=user_id,
        product_id=product_id,
        rating=rating,
        title=data.get("title", ""),
        comment=data.get("comment", ""),
    )
    db.session.add(review)
    db.session.commit()

    return jsonify({"message": "Review submitted", "review": review.to_dict()}), 201


@review_bp.route("/<int:review_id>", methods=["PUT"])
@jwt_required()
def update_review(review_id):
    """Update own review."""
    user_id = int(get_jwt_identity())
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    if review.user_id != user_id:
        return jsonify({"error": "You can only edit your own reviews"}), 403

    data = request.get_json()
    if "rating" in data:
        rating = int(data["rating"])
        if rating < 1 or rating > 5:
            return jsonify({"error": "Rating must be between 1 and 5"}), 400
        review.rating = rating
    if "title" in data:
        review.title = data["title"]
    if "comment" in data:
        review.comment = data["comment"]

    db.session.commit()
    return jsonify({"message": "Review updated", "review": review.to_dict()}), 200


@review_bp.route("/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(review_id):
    """Delete own review."""
    user_id = int(get_jwt_identity())
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    if review.user_id != user_id:
        return jsonify({"error": "You can only delete your own reviews"}), 403

    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted"}), 200
