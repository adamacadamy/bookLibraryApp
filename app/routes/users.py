from http import HTTPStatus
from flask_login import logout_user
from flask_restx import Namespace, Resource
from flask import request

from app.schemas.user_schema import user_model, user_login_model
from app.models import db
from app.models.user import User 

users_ns = Namespace("User", description="User  management")

# user crud = [create, read, update , delete]

class UsersList(Resource):
    pass

class UsersResource(Resource):
    pass
