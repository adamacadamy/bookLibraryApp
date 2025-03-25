from http import HTTPStatus
from flask_restx import Namespace, Resource
from flask import Response, g, request

from app.schemas.user_schema import (
    user_response_schema,
    user_request_model_schema,
    user_schema,
    user_update_request_model_schema,
    user_query_parser,
)
from app.models import db
from app.models.user import User, UserRole

from app.utils.auth_utils import auth_required
from app.utils.emai import send_registration_email

users_ns = Namespace("User", description="User management")


@users_ns.route("/")
class UsersList(Resource):

    @users_ns.expect(user_query_parser, validate=True)
    @users_ns.response(HTTPStatus.OK, "List of users", user_response_schema)
    @users_ns.doc(security=["basic", "jwt"])
    @auth_required([UserRole.ADMIN, UserRole.USER])
    def get(self) -> Response:
        """Retrieve a list of users with pagination and filtering."""
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        username = request.args.get("username", type=str)
        email = request.args.get("email", type=str)
        role = request.args.get("role", type=str)

        query = User.query
        if username:
            query = query.filter(User.username.ilike(f"%{username}%"))
        if email:
            query = query.filter(User.email.ilike(f"%{email}%"))
        if role:
            query = query.filter(User.role.ilike(f"%{role}%"))

        users_query = query.paginate(page=page, per_page=per_page, error_out=False)
        users = users_query.items

        return {
            "success": True,
            "data": [user.to_dict() for user in users],
            "total": users_query.total,
            "pages": users_query.pages,
            "current_page": users_query.page,
            "per_page": users_query.per_page,
        }, HTTPStatus.OK

    @users_ns.expect(user_request_model_schema, validate=True)
    @users_ns.response(HTTPStatus.CREATED, "User created", user_schema)
    @users_ns.response(HTTPStatus.BAD_REQUEST, "Invalid input")
    @users_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @users_ns.response(HTTPStatus.FORBIDDEN, "Forbidden")
    @users_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @users_ns.doc(security=["basic", "jwt"])
    @auth_required([UserRole.ADMIN])
    def post(self) -> Response:
        """Add a new user to the database (admin only)."""
        data = request.json
        if "password" not in data:
            data["password"] = User.generate_random_password()

        user = User(**data)
        db.session.add(user)
        db.session.commit()
        try:
            send_registration_email(
                user.email, user.full_name, user.username, data["password"]
            )
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return {"success": True, "data": user.to_dict()}, HTTPStatus.CREATED


@users_ns.route("/me")
class MeResource(Resource):
    @users_ns.expect(user_update_request_model_schema, validate=True)
    @users_ns.response(HTTPStatus.ACCEPTED, "User found", user_schema)
    @users_ns.response(HTTPStatus.NOT_FOUND, "User not found")
    @users_ns.response(HTTPStatus.BAD_REQUEST, "Invalid input")
    @users_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @users_ns.response(HTTPStatus.FORBIDDEN, "Forbidden")
    @users_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @users_ns.doc(security=["basic", "jwt"])
    @auth_required([UserRole.ADMIN, UserRole.USER])
    def put(self) -> Response:
        """Update the currently authenticated user."""
        user_id = g.current_user["user_id"]

        user = User.load_user(user_id)
        data = request.json
        if not user:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND

        if user.role == UserRole.ADMIN:
            user = User.update_user_as_admin(user, data)
        if user.role == UserRole.USER:
            user = User.update_user_as_user(user, data)

        db.session.commit()

        return {"success": True, "data": user.to_dict()}, HTTPStatus.OK

    @users_ns.response(HTTPStatus.NO_CONTENT, "User deleted")
    @users_ns.response(HTTPStatus.NOT_FOUND, "User not found")
    @users_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @users_ns.response(HTTPStatus.FORBIDDEN, "Forbidden")
    @users_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @users_ns.doc(security=["basic", "jwt"])
    @auth_required([UserRole.ADMIN, UserRole.USER])
    def delete(self) -> Response:
        """Delete the currently authenticated user."""
        user_id = g.current_user["user_id"]
        user = User.load_user(user_id)
        if not user:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND

        user.is_active = False
        db.session.commit()
        return {"success": True}, HTTPStatus.NO_CONTENT


@users_ns.route("/<int:user_id>")
class UsersResource(Resource):
    @users_ns.response(HTTPStatus.OK, "User found", user_schema)
    @users_ns.response(HTTPStatus.NOT_FOUND, "User not found")
    @users_ns.response(HTTPStatus.BAD_REQUEST, "Invalid input")
    @users_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @users_ns.response(HTTPStatus.FORBIDDEN, "Forbidden")
    @users_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @users_ns.doc(security=["basic", "jwt"])
    @auth_required([UserRole.ADMIN, UserRole.USER])
    def get(self, user_id: int) -> Response:
        """Retrieve a specific user by ID."""
        user = User.load_user(user_id)

        if user.role != UserRole.ADMIN or user.id != id:
            return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

        return {"success": True, "data": user.to_dict()}, HTTPStatus.OK

    @users_ns.expect(user_update_request_model_schema, validate=True)
    @users_ns.response(HTTPStatus.ACCEPTED, "User found", user_schema)
    @users_ns.response(HTTPStatus.NOT_FOUND, "User not found")
    @users_ns.response(HTTPStatus.BAD_REQUEST, "Invalid input")
    @users_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @users_ns.response(HTTPStatus.FORBIDDEN, "Forbidden")
    @users_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @users_ns.doc(security=["basic", "jwt"])
    @auth_required([UserRole.ADMIN])
    def put(self, user_id: int) -> Response:
        """Update an existing user."""
        user = User.load_user(user_id)

        if not user:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND

        user.is_active = False

        db.session.commit()

        return {"success": True, "data": user.to_dict()}, HTTPStatus.OK

    @users_ns.response(HTTPStatus.NO_CONTENT, "User deleted")
    @users_ns.response(HTTPStatus.NOT_FOUND, "User not found")
    @users_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @users_ns.response(HTTPStatus.FORBIDDEN, "Forbidden")
    @users_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @users_ns.doc(security=["basic", "jwt"])
    @auth_required([UserRole.ADMIN])
    def delete(self, user_id: int) -> Response:
        """Delete a user from the database (admin only)."""
        user = User.load_user(user_id)
        if not user:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND

        if user.role == UserRole.ADMIN:
            return {"message": "Forbidden"}, HTTPStatus.FORBIDDEN
        db.session.delete(user)
        db.session.commit()
        return {"success": True}, HTTPStatus.NO_CONTENT
