from enum import Enum
import logging
import secrets
import string
from flask_login import UserMixin

from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash

# Correct the logging level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Enum for User Roles
class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "username": self.username,
            "role": self.role.value,
        }

    @staticmethod
    def generate_random_password(length: int = 8) -> str:
        characters = string.ascii_letters + string.digits + string.punctuation
        return "".join(secrets.choice(characters) for _ in range(length))

    @staticmethod
    def check_password(password_hash: str, password: str) -> bool:
        return check_password_hash(password_hash, password)

    @staticmethod
    def create_user(
        full_name: str, username: str, email: str, password: str, role: UserRole
    ) -> "User":
        hashed_password = generate_password_hash(password)
        return User(
            full_name=full_name,
            username=username,
            password=hashed_password,
            email=email,
            role=role,
        )

    @staticmethod
    def update_user_as_admin(user: "User", data: dict) -> "User":
        if "password" in data:
            data["password"] = generate_password_hash(data["password"])
        if "role" in data:
            data["role"] = UserRole(data["role"])
        if "full_name" in data:
            user.full_name = data["full_name"]
        if "username" in data:
            user.username = data["username"]
        if "email" in data:
            user.email = data["email"]
        if "role" in data:
            user.role = data["role"]
        return user

    @staticmethod
    def update_user_as_user(user: "User", data: dict) -> "User":
        if "password" in data:
            data["password"] = generate_password_hash(data["password"])
        if "full_name" in data:
            user.full_name = data["full_name"]
        if "username" in data:
            user.username = data["username"]
        if "email" in data:
            user.email = data["email"]
        return user

    @staticmethod
    def load_user(user_id: int) -> "User":
        return User.query.get(int(user_id))

    @staticmethod
    def create_admin_user(app: Flask):
        with app.app_context():
            db.create_all()
            admin_username = "admin"
            admin_email = "admin@admin.com"
            admin_password = "admin123"  # Change this to a secure password
            admin_full_name = "Administrator"

            # Check if the admin user already exists
            admin_user = User.query.filter_by(username=admin_username).first()
            if not admin_user:
                admin_user = User.create_user(
                    full_name=admin_full_name,
                    username=admin_username,
                    email=admin_email,
                    password=admin_password,
                    role=UserRole.ADMIN,
                )
                db.session.add(admin_user)
                db.session.commit()
                logger.info(f"Admin user '{admin_username}' created successfully.")
            else:
                logger.info(f"Admin user '{admin_username}' already exists.")
