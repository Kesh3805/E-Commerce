from app.extensions import db
from datetime import datetime, timezone
import json


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    compare_price = db.Column(db.Float, nullable=True)  # original / strikethrough price
    stock = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(500), nullable=True)
    images = db.Column(db.Text, nullable=True)  # JSON array of image URLs
    brand = db.Column(db.String(100), nullable=True, index=True)
    sku = db.Column(db.String(50), nullable=True, unique=True)
    is_featured = db.Column(db.Boolean, default=False, index=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    category = db.relationship("Category", backref=db.backref("products", lazy="dynamic", overlaps="category"), overlaps="products")
    reviews = db.relationship("Review", backref="reviewed_product", lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    @property
    def is_available(self):
        return self.stock > 0 and self.is_active

    @property
    def is_low_stock(self):
        return 0 < self.stock < 10

    @property
    def stock_status(self):
        if not self.is_active:
            return "unavailable"
        if self.stock == 0:
            return "out_of_stock"
        elif self.stock < 10:
            return "low_stock"
        return "in_stock"

    @property
    def discount_percent(self):
        if self.compare_price and self.compare_price > self.price:
            return round((1 - self.price / self.compare_price) * 100)
        return 0

    @property
    def avg_rating(self):
        from sqlalchemy import func
        result = db.session.query(func.avg(db.literal_column('rating'))).filter(
            db.literal_column('product_id') == self.id
        ).select_from(db.Table('reviews', db.metadata, autoload_with=db.engine)).scalar()
        return round(float(result), 1) if result else 0

    @property
    def review_count(self):
        return self.reviews.count() if self.reviews else 0

    @property
    def image_list(self):
        if self.images:
            try:
                return json.loads(self.images)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    def to_summary(self):
        """Lightweight dict for list views."""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "compare_price": self.compare_price,
            "discount_percent": self.discount_percent,
            "image_url": self.image_url,
            "brand": self.brand,
            "is_featured": self.is_featured,
            "stock_status": self.stock_status,
            "category_id": self.category_id,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "compare_price": self.compare_price,
            "discount_percent": self.discount_percent,
            "stock": self.stock,
            "image_url": self.image_url,
            "images": self.image_list,
            "brand": self.brand,
            "sku": self.sku,
            "is_featured": self.is_featured,
            "is_active": self.is_active,
            "category_id": self.category_id,
            "category": self.category.name if self.category else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_available": self.is_available,
            "stock_status": self.stock_status,
        }
