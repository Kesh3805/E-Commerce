from app.extensions import db
from datetime import datetime, timezone
import json


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    total_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=True)
    discount_amount = db.Column(db.Float, default=0)
    coupon_code = db.Column(db.String(50), nullable=True)
    shipping_address = db.Column(db.Text, nullable=True)  # JSON
    payment_method = db.Column(db.String(30), default="COD")  # COD / CARD / UPI
    tracking_number = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="PLACED")
    # PLACED / PROCESSING / SHIPPED / DELIVERED / CANCELLED
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    items = db.relationship("OrderItem", backref="order", lazy="joined", cascade="all, delete-orphan")

    @property
    def address_dict(self):
        if self.shipping_address:
            try:
                return json.loads(self.shipping_address)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "total_price": self.total_price,
            "subtotal": self.subtotal,
            "discount_amount": self.discount_amount,
            "coupon_code": self.coupon_code,
            "shipping_address": self.address_dict,
            "payment_method": self.payment_method,
            "tracking_number": self.tracking_number,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "items": [item.to_dict() for item in self.items],
        }


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Relationship
    product = db.relationship("Product", backref="order_items", lazy="joined")

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price": self.price,
            "product": self.product.to_dict() if self.product else None,
        }
