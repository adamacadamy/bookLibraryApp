from http import HTTPStatus
from flask_login import logout_user
from flask_restx import Namespace, Resource
from flask import request

from app.schemas.user_schema import user_model, user_login_model
from app.models import db
from app.models.user import User 

auth_ns = Namespace("User", description="Authentication management")
 

# login 
class Login(Resource):
    pass

# lgout
class Logout(Resource):
    pass