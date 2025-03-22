from app.models import db

class Book(db.Model): 
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    available = db.Column(db.Boolean, default=True)
    borrowed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    borrowed_unilt = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "image": self.image,
            "author": self.author,
            "isbn": self.isbn,
            "available": self.available,
            "borrowed_by": self.borrowed_by,
            "borrowed_unilt": self.borrowed_unilt.isoformat() if self.borrowed_unilt is not None else ""
        }
 