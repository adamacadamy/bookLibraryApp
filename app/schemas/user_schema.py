from attr import fields
from app.schemas import api

user_model_schema = api.model(
    "UserModel",
    {
        "id": fields.Integer(readonly=True, description="User ID"),
        "username": fields.String(required=True, description="Username"),
        "email": fields.String(required=True, description="Email"),
        "password": fields.String(required=True, description="Password"),
        "role": fields.String(required=True, description="User role (e.g., admin, user)"),
    },
)

user_login_schema = api.model('UserLoginModel', { 
    "username": fields.String(required=True, description="Username"),
    "password": fields.String(required=True, description="Password"),
})