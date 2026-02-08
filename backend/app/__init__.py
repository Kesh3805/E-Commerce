from flask import Flask
from flask_cors import CORS
from app.extensions import db, jwt, bcrypt, migrate
from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, supports_credentials=True)

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.product_routes import product_bp
    from app.routes.cart_routes import cart_bp
    from app.routes.order_routes import order_bp
    from app.routes.category_routes import category_bp
    from app.routes.review_routes import review_bp
    from app.routes.wishlist_routes import wishlist_bp
    from app.routes.address_routes import address_bp
    from app.routes.coupon_routes import coupon_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(product_bp, url_prefix="/api/products")
    app.register_blueprint(cart_bp, url_prefix="/api/cart")
    app.register_blueprint(order_bp, url_prefix="/api/orders")
    app.register_blueprint(category_bp, url_prefix="/api/categories")
    app.register_blueprint(review_bp, url_prefix="/api/reviews")
    app.register_blueprint(wishlist_bp, url_prefix="/api/wishlist")
    app.register_blueprint(address_bp, url_prefix="/api/addresses")
    app.register_blueprint(coupon_bp, url_prefix="/api/coupons")

    # Create tables
    with app.app_context():
        from app.models import (user, product, cart, order,
                                category, review, wishlist, address, coupon)  # noqa: F401
        db.create_all()

    return app
