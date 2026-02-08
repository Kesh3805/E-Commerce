from app.extensions import db
from datetime import datetime, timezone


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    avatar = db.Column(db.String(500), nullable=True)
    role = db.Column(db.String(10), nullable=False, default="USER")  # USER / ADMIN
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    cart_items = db.relationship("Cart", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    orders = db.relationship("Order", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    wishlist = db.relationship("Wishlist", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    addresses = db.relationship("Address", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    reviews = db.relationship("Review", backref="reviewer", lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "avatar": self.avatar,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
