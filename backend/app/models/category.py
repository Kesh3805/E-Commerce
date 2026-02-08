from app.extensions import db
from datetime import datetime, timezone


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Self-referential for subcategories
    subcategories = db.relationship("Category", backref=db.backref("parent", remote_side="Category.id"), lazy="dynamic")

    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)

    def to_dict(self, include_children=False):
        data = {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "image_url": self.image_url,
            "parent_id": self.parent_id,
            "product_count": self.products.count(),
        }
        if include_children:
            data["subcategories"] = [c.to_dict() for c in self.subcategories]
        return data
