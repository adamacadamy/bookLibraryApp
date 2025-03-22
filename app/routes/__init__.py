from flask_restx import Api
from flask import Flask

from app.routes.auth import auth_ns
from app.routes.users import users_ns
from app.routes.books import books_ns, books_borrow_ns, books_return_ns

def register_routes(api: Api, app: Flask) -> None:

    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(users_ns, path="/user")
    api.add_namespace(books_ns, path="/book")
    api.add_namespace(books_borrow_ns, path="/barrow")
    api.add_namespace(books_return_ns, path="/return")
 