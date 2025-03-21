## BOOK LIBRARY APP

A Book Library App is a software application designed to manage a collection of books.

## Specification

## 1. Data Model

### 1.1. User model

- `id` (Primary Key)
- `username` (String, Unique)
- `password` (String, Hashed)
- `Role`  (Enum)

## 2.2 Book Model

- `id` (Primary Key)
- `author` (String Unique)
- `isbn` (String Unique)
- `available` (Bool)
- `borrowed_by` (Foreign Key)


## 2. Activities [BL(Business Logic)]
- Register User by admin
- Add, Delete, Update a book as an admin
- Read/View Books as guest, admin or user
- Barrow/Return books as guest


## 3. REST API

## 3.1 User management Endpoints  
 
| Method | Path         | Description             | Roles               |
|--------|--------------|-------------------------|---------------------|
| POST   | `/register`  | Register a new user     | Admin               |
| POST   | `/update`    | Register a new user     | Admin               |
| POST   | `/delete`    | Register a new user     | Admin               |
| POST   | `/view`      | Register a new user     | Admin               |
| POST   | `/login`     | Authenticate user       | Admin, Guest, User  |  


## 3.2 Book CREATE AND READ Endpoints [ books_list.py]

| Method  | Path                   | Description              | Roles              |
|---------|------------------------|--------------------------|--------------------|
| POST    | `/book`                | Register a new book      | Admin              |
| GET     | `/book`                | View list of books       | Admin, Guest, User |

## 3.3 Book UPDATE AND DELETE Endpoints 

| Method  | Path                   | Description              | Roles              |
|---------|------------------------|--------------------------|--------------------|
| PUT     | `/book/<int:book_id>`  | Update a book            | Admin              |
| DELETE  | `/book/<int:book_id>`  | Delete a book            | Admin              |

## 3.3 Book BARROW AND RETURN Endpoints  

| Method  | Path                   | Description              | Roles              |
|---------|------------------------|--------------------------|--------------------|
| POST    | `/barrow/<int:book_id>`| Borrow a book            | User               |
| POST    | `/return/<int:book_id>`| Return a book            | User               |


## 3.4 Schemas

#### 3.3.1 User Schema

- `id` (Integer, ReadOnly)
- `username` (String, Required)
- `email` (String, Required, Unique)
- `password` (String, Required)
- `Role` (String, Required)

#### 3.4.2 User login Schema  

- `username` (String, Required)
- `password` (String, Required)

### 3.4.3 Book Schema

- `id` (Integer, ReadOnly)
- `title` (String, Required)
- `author` (String, Required)
- `isbn` (String, Required)
- `available` (Boolean, ReadOnly)
- `borrowed_by` (Integer, ReadOnly)

#### 3.4.4 Book Request Schema

- `title` (String, Required)
- `author` (String, Required)
- `isbn` (String, Required)

#### 3.4.5 Book Response Schema

- `success` (Boolean)
- `data` (Nested, Book Schema, SkipNone=True)

#### 3.4.6 Book List Schema

- `success` (Boolean)
- `data` (List, Nested Book Schema)
- `total` (Integer)
- `pages` (Integer)

#### 3.4.7 Book Borrow Schema

- `message` (String, Required)
- `user` (String, Required)
- `book` (String, Required)


## 5. Scaffold Structure

```text
book-library-app/
├── .gitignore               # Ignore unnecessary files
├── .env                     # Environment variables
├── .vscode/                 # VSCode settings
│   ├── settings.json        # Workspace settings
│   └── launch.json          # Debugging configurations
├── app/                     # Application logic
│   ├── __init__.py          # Initialize Flask app
│   ├── utils/               # Database models
│   │   ├── __init__.py      # package file
│   │   ├── auth_utils.py    # User authentication utilities
│   ├── models/              # Database models
│   │   ├── __init__.py      # Initialize models
│   │   ├── user.py          # User model
│   │   └── books.py         # Book model
│   ├── routes/              # Application routes
│   │   ├── __init__.py      # Initialize routes
│   │   ├── auth.py          # Authentication routes
|   |   ├── book_items.py    # Book update and delete
|   |   ├── books_list.pyy   # Book create and view
|   |   ├── book_cycle.py    # Book borrow and return
|   |   ├── users.py         # User crud
│   ├── schemas/             # API schemas
│   │   ├── __init__.py      # Initialize schemas
│   │   ├── user_schema.py   # User schema
│   │   └── book_schema.py   # ToDo schema
├── migrations/              # Flask-Migrate folder
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md                # Project documentation
```

## 6. JSON  version of the scaffold
```json
{
    ".gitignore": "",
    ".env": "",
    ".vscode": {
        "settings.json": "",
        "launch.json": ""
    },
    "app": {
        "__init__.py": "",
        "utils": {
            "__init__.py": "",
            "auth_utils.py": ""
        },
        "models": {
            "__init__.py": "",
            "user.py": "",
            "books.py": ""
        },
        "routes": {
            "__init__.py": "",
            "auth.py": "",
            "book_items.py": "",
            "books_list.py": "",
            "book_cycle.py": "",
            "users.py": ""
        },
        "schemas": {
            "__init__.py": "",
            "user_schema.py": "",
            "book_schema.py": ""
        }
    },
    "migrations": {},
    "requirements.txt": "alembic==1.14.0\naniso8601==9.0.1\nattrs==24.3.0\nblinker==1.9.0\nclick==8.1.7\nFlask==2.2.5\nFlask-HTTPAuth==4.8.0\nFlask-JWT-Extended==4.4.4\nFlask-Login==0.6.3\nFlask-Migrate==4.0.4\nflask-restx==1.3.0\nFlask-SQLAlchemy==3.1.1\nFlask-WTF==1.2.2\ngreenlet==3.1.1\nimportlib_resources==6.4.5\nitsdangerous==2.2.0\nJinja2==3.1.4\njsonschema==4.23.0\njsonschema-specifications==2024.10.1\nMako==1.3.8\nMarkupSafe==3.0.2\nmysql-connector-python==8.0.33\nmysqlclient==2.2.7\nprotobuf==3.20.3\nPyJWT==2.10.1\nPyMySQL==1.1.1\npython-dotenv==1.0.0\npytz==2024.2\nreferencing==0.35.1\nrpds-py==0.22.3\nSQLAlchemy==2.0.36\ntyping_extensions==4.12.2\nWerkzeug==3.1.3\nWTForms==3.2.1",
    "run.py": "",
    "README.md": ""
}
```

## 8. Run Scaffold generator
```python
python3 create_flask_project.py book_library_structure.json -d book-library-app
```