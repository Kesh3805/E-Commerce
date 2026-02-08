from app.extensions import db
from datetime import datetime, timezone


class Coupon(db.Model):
    __tablename__ = "coupons"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    discount_type = db.Column(db.String(10), nullable=False, default="percent")  # percent / flat
    discount_value = db.Column(db.Float, nullable=False)
    min_order_amount = db.Column(db.Float, nullable=False, default=0)
    max_discount = db.Column(db.Float, nullable=True)                             # cap for percent
    usage_limit = db.Column(db.Integer, nullable=True)
    times_used = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, default=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, **kwargs):
        super(Coupon, self).__init__(**kwargs)

    @property
    def is_valid(self):
        if not self.is_active:
            return False
        if self.usage_limit and self.times_used >= self.usage_limit:
            return False
        if self.expires_at and datetime.now(timezone.utc) > self.expires_at:
            return False
        return True

    def calculate_discount(self, order_total):
        if order_total < self.min_order_amount:
            return 0
        if self.discount_type == "percent":
            discount = order_total * (self.discount_value / 100)
            if self.max_discount:
                discount = min(discount, self.max_discount)
        else:
            discount = self.discount_value
        return round(min(discount, order_total), 2)

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "discount_type": self.discount_type,
            "discount_value": self.discount_value,
            "min_order_amount": self.min_order_amount,
            "max_discount": self.max_discount,
            "usage_limit": self.usage_limit,
            "times_used": self.times_used,
            "is_active": self.is_active,
            "is_valid": self.is_valid,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }
