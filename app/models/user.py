from app.models import db
from app.utils.auth_utils import UserRole
from werkzeug.security  import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) 
    role = db.Column(db.Enum(UserRole), nullable=False)
    
    def to_dict(self):
        return {"id": self.id, "username": self.username, "role": self.role.value}
    

    @staticmethod
    def check_password(password_hash: str, password: str )-> bool:
        return check_password_hash(password_hash, password)
        

    @staticmethod
    def create_user(username: str, email: str, password: str, role: UserRole):
        hashed_password = generate_password_hash(password)
        return  User(
            username=username,
            password=hashed_password,
            email=email,
            role=role
        )
    
    @staticmethod
    def load_user(user_id: int) -> "User":
        return User.query.get(int(user_id))