from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.schemas import api
from app.utils.date_utils import date_type

book_schema_parser = reqparse.RequestParser()

book_request_schema_parser = reqparse.RequestParser()

book_schema_parser.add_argument('id', type=int, required=False) 
book_schema_parser.add_argument('title', type=str, required=True, help="Book title is required") 
book_schema_parser.add_argument('description', type=str, required=True, help="Book description is requireed") 
book_schema_parser.add_argument('image', type=FileStorage, required=True, location='files', help='Image file is required') 
book_schema_parser.add_argument('author', type=str, required=True, help="Book author is requireed") 
book_schema_parser.add_argument('isbn', type=str, required=True, help="Book isbn number is requireed") 
book_schema_parser.add_argument('available', type=bool, required=False, help="Book availablity in boolean is requireed") 
book_schema_parser.add_argument('borrowed_by', type=int, required=False, help="Book borrower id in int is requireed") 
book_schema_parser.add_argument('borrowed_unilt', type=date_type, required=False, help='Date in YYYY-MM-DD format')
 


book_request_schema_parser.add_argument('title', type=str, required=True, help="Book title is required") 
book_request_schema_parser.add_argument('description', type=str, required=True, help="Book description is requireed") 
book_request_schema_parser.add_argument('image', type=FileStorage, required=True, location='files', help='Image file is required') 
book_request_schema_parser.add_argument('author', type=str, required=True, help="Book author is requireed") 
book_request_schema_parser.add_argument('isbn', type=str, required=True, help="Book isbn number is requireed") 

book_schema = api.model('BookModel', {
    "id": fields.Integer(readonly=True),
    "title": fields.String(required=True),
    "author": fields.String(required=True),
    "description": fields.String(required=True),
    "isbn": fields.String(required=True),
    "available": fields.Boolean(readonly=True),
    "borrowed_by": fields.Integer(readonly=True),
    "borrowed_unilt": fields.String(readonly=True),
})


book_response_schema = api.model('BookResponseModel', {
    "success": fields.Boolean(),
    "data": fields.Nested(book_schema, skip_none=True), 
})

book_list_schema =  api.model('BookListResponseModel', {
    "success": fields.Boolean(),
    "data": fields.List(fields.Nested(book_schema)),
    "total": fields.Integer(),
    "pages": fields.Integer()
})

book_borrow_schema =  ('BookBorrowResponseModel', {
    "message": fields.String(required=True),
    "user":  fields.String(required=True),
    "book":   fields.String(required=True),
    "borrowed_unilt": fields.Date(required=True),
  })
