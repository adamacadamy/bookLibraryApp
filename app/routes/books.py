from http import HTTPStatus
import logging
import mimetypes
import os
from flask_restx import Namespace, Resource
from flask import Response, g, request, send_file

from app.config.uploads import UPLOAD_FOLDER
from app.models.books import Book
from app.models import db
from app.models.user import User

from app.schemas.book_schema import (
    book_list_schema,
    book_schema_parser,
    book_response_schema,
    book_borrow_schema,
    book_request_schema_parser,
)
from app.models.user import UserRole

from app.utils.auth_utils import auth_required
from app.utils.files import save_file_to_upload_folder


# Correct the logging level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


books_ns = Namespace("Book", description="Book  management")


# /api/Book/?page=1&per_page=10
# /api/Book/?title=Harry&author=Rowling&genre=Fantasy.
# /api/Book/?page=1&per_page=10&title=Harry&author=Rowling&genre=Fantasy.
@books_ns.route("/")
class BooksList(Resource):
    @books_ns.response(HTTPStatus.OK, "Books retrieved", book_list_schema)
    def get(self) -> Response:
        # Get query parameters for pagination
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        # Get query parameters for filtering
        title = request.args.get("title", type=str)
        author = request.args.get("author", type=str)
        genre = request.args.get("genre", type=str)

        # Build the query with optional filters
        query = Book.query
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))
        if genre:
            query = query.filter(Book.genre.ilike(f"%{genre}%"))

        # Apply pagination
        books_query = query.paginate(page=page, per_page=per_page, error_out=False)
        books = books_query.items

        return {
            "success": True,
            "data": [book.to_dict() for book in books],
            "total": books_query.total,
            "pages": books_query.pages,
            "current_page": books_query.page,
            "per_page": books_query.per_page,
        }, HTTPStatus.OK

    @books_ns.expect(book_schema_parser, validate=True)
    @books_ns.response(HTTPStatus.CREATED, "Book added", book_response_schema)
    @books_ns.response(HTTPStatus.BAD_REQUEST, "Invalid input")
    @books_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @books_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server issue")
    @books_ns.doc(security=["basic", "jwt"])
    @auth_required([UserRole.ADMIN])
    def post(self) -> Response:
        try:
            # Save the file
            args = book_schema_parser.parse_args()
            image_file = args["image"]
            image = save_file_to_upload_folder(image_file)  # URL to access the image
            title = args["title"]
            author = args["author"]
            description = args["description"]
            isbn = args["isbn"]

            book = Book(
                title=title,
                author=author,
                description=description,
                isbn=isbn,
                image=image,
            )
            db.session.add(book)
            db.session.commit()
            return {"success": True, "data": book.to_dict()}, HTTPStatus.OK
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return {
                "success": False,
                "message": str(e),
            }, HTTPStatus.INTERNAL_SERVER_ERROR


@books_ns.route("/<int:id>")
class BooksResource(Resource):
    @books_ns.response(HTTPStatus.OK, "Book retrieved", book_response_schema)
    @books_ns.response(HTTPStatus.NOT_FOUND, "Book not found")
    @books_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @books_ns.doc(security=["basic", "jwt"])
    @auth_required([UserRole.ADMIN, UserRole.USER])
    def get(self, id: int) -> Response:
        book = Book.query.get(id)
        if book:
            return {"success": True, "data": book.to_dict()}, HTTPStatus.OK
        return {"success": False, "message": "Book not found"}, HTTPStatus.NOT_FOUND

    @books_ns.expect(book_request_schema_parser, validate=True)
    @books_ns.response(HTTPStatus.CREATED, "Book updated", book_response_schema)
    @books_ns.response(HTTPStatus.BAD_REQUEST, "Invalid input")
    @books_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @books_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server issue")
    @books_ns.doc(security=["basic", "jwt"])
    @auth_required([UserRole.ADMIN])
    def put(self, id: int) -> Response:
        args = book_schema_parser.parse_args()
        book = Book.query.get(id)
        try:
            if book:
                if image := args.get("image"):
                    book.image = save_file_to_upload_folder(image)
                if title := args.get("title"):
                    book.title = title
                if author := args.get("author"):
                    book.author = author
                if description := args.get("description"):
                    book.description = description
                if isbn := args.get("isbn"):
                    book.isbn = isbn
                if available := args.get("available"):
                    book.available = available
                db.session.commit()
                return {"success": True, "data": book.to_dict()}, HTTPStatus.OK
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return {
                "message": f"An error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        return {"success": False}, HTTPStatus.NOT_FOUND

    @books_ns.response(HTTPStatus.OK, "Book deleted")
    @books_ns.response(HTTPStatus.NOT_FOUND, "Book not found")
    @books_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @books_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server issue")
    @books_ns.doc(security=["basic", "jwt"])
    @auth_required([UserRole.ADMIN])
    def delete(self, id: int) -> Response:
        book = Book.query.get(id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return {"success": True}, HTTPStatus.OK
        return {"success": False, "message": "Book not found"}, HTTPStatus.NOT_FOUND


@books_ns.route("/images/<string:filename>")
class BookServeImage(Resource):
    @books_ns.response(HTTPStatus.OK, "Image retrieved")
    @books_ns.response(HTTPStatus.NOT_FOUND, "Image not found")
    @books_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server issue")
    def get(self, filename: str) -> Response:
        try:
            # Construct the full path to the image
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            # Check if the file exists
            if not os.path.exists(file_path):
                return {"message": "Image not found"}, HTTPStatus.NOT_FOUND

            # Determine the MIME type based on the file extension
            mime_type, _ = mimetypes.guess_type(file_path)

            # Serve the image file
            return send_file(file_path, mimetype=mime_type)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return {
                "message": f"An error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR


@books_ns.route("/barrow/<int:book_id>")
class BookBorrowResrouce(Resource):
    @books_ns.response(HTTPStatus.CREATED, "Book borrowed", book_borrow_schema)
    @books_ns.response(HTTPStatus.BAD_REQUEST, "Invalid input")
    @books_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @books_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server issue")
    @books_ns.doc(security=["basic, jwt"])
    @auth_required([UserRole.ADMIN, UserRole.USER])
    def update(self, book_id: int) -> Response:
        try:
            args = book_schema_parser.parse_args()
            book = Book.query.get(book_id)
            user_id = g.current_user["id"]
            user = User.query.get(user_id)
            if book and user:
                book.borrowed_by = user.id
                book.borrowed_until = args["borrowed_until"]
                book.available = False
                db.session.commit()
                return {
                    "message": "Book borrowed",
                    "user": user.username,
                    "book": book.title,
                    "borrowed_until": book.borrowed_until,
                }, HTTPStatus.CREATED
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return {
                "message": f"An error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        return {"message": "Book not found"}, HTTPStatus.NOT_FOUND


@books_ns.route("/return/<int:id>")
class BookReturnResrouce(Resource):
    @books_ns.response(HTTPStatus.CREATED, "Book returned")
    @books_ns.response(HTTPStatus.BAD_REQUEST, "Invalid input")
    @books_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @books_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server issue")
    @books_ns.doc(security=["basic, jwt"])
    @auth_required([UserRole.ADMIN, UserRole.USER])
    def update(self, id: int) -> Response:
        book = Book.query.get(id)
        if book:
            book.borrowed_by = None
            book.borrowed_until = None
            book.available = True
            db.session.commit()
            return {"message": "Book returned"}, HTTPStatus.CREATED
        return {"message": "Book not found"}, HTTPStatus.NOT_FOUND
