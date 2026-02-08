from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.user import User


def admin_required(fn):
    """Decorator to restrict access to admin users only."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != "ADMIN":
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


def validate_required_fields(data, fields):
    """Validate that all required fields are present and non-empty."""
    missing = [f for f in fields if not data.get(f)]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, None


def validate_price(price):
    """Validate that price is a positive number."""
    try:
        price_float = float(price)
        if price_float <= 0:
            return False, "Price must be greater than 0"
        return True, price_float
    except (ValueError, TypeError):
        return False, "Invalid price format"


def validate_stock(stock):
    """Validate that stock is a non-negative integer."""
    try:
        stock_int = int(stock)
        if stock_int < 0:
            return False, "Stock cannot be negative"
        return True, stock_int
    except (ValueError, TypeError):
        return False, "Invalid stock format"


def format_currency(amount):
    """Format amount as currency string."""
    return f"${amount:.2f}"


def calculate_order_total(items):
    """Calculate total price for order items."""
    return sum(item.price * item.quantity for item in items)
