from app.extensions import db
from datetime import datetime, timezone


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)          # 1-5
    title = db.Column(db.String(200), nullable=True)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint("user_id", "product_id", name="uq_user_product_review"),
        db.CheckConstraint("rating >= 1 AND rating <= 5", name="ck_rating_range"),
    )

    def __init__(self, **kwargs):
        super(Review, self).__init__(**kwargs)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "rating": self.rating,
            "title": self.title,
            "comment": self.comment,
            "user_name": self.reviewer.name if self.reviewer else "Anonymous",
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
