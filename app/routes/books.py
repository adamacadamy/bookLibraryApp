from http import HTTPStatus
from flask_login import logout_user
from flask_restx import Namespace, Resource
from flask import request

from app.schemas.user_schema import user_model, user_login_model
from app.models import db
from app.models.user import User 

books_ns = Namespace("User", description="Book  management")
books_borrow_ns = Namespace("User", description="Book borrow management")
books_return_ns = Namespace("User", description="Book return  management")

class BooksList(Resource):
    pass

class BooksResource(Resource):
    pass

class BookBorrowResrouce(Resource):
    pass

class BookReturnResrouce(Resource):
    pass

