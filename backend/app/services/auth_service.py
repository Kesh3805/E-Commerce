import re
from app.extensions import db, bcrypt
from app.models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token


class AuthService:

    @staticmethod
    def register(name, email, password, role="USER"):
        # Validate email format
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            return None, "Invalid email format"

        # Check password strength
        if len(password) < 6:
            return None, "Password must be at least 6 characters"

        # Check if email already exists
        if User.query.filter_by(email=email.lower().strip()).first():
            return None, "Email already registered"

        # Validate role
        if role not in ("USER", "ADMIN"):
            return None, "Invalid role"

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(
            name=name.strip(),
            email=email.lower().strip(),
            password_hash=password_hash,
            role=role,
        )
        db.session.add(user)
        db.session.commit()

        return user, None

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email.lower().strip()).first()
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return None, None, "Invalid email or password"

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return access_token, refresh_token, None

    @staticmethod
    def get_profile(user_id):
        user = User.query.get(user_id)
        if not user:
            return None, "User not found"
        return user, None
