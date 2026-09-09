from flask import Flask, request
from extensions import db
from services import get_all_books, get_book_by_id, add_book, update_book as update_book_service, delete_book as delete_book_service
from flasgger import Swagger


app = Flask(__name__)
swagger = Swagger(app)

#َadd database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
db.init_app(app)


with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Flask connected to database!"

@app.route("/books", methods=["POST"])
def add_books():
    """
    Add a new book
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: book
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
            price:
              type: number
            published_year:
              type: integer
    responses:
      201:
        description: Book added successfully
     """
    
    data = request.json
    book = add_book(data)
    
    return {"message": "Book added successfully",
            "id": book.id}, 201
    

@app.route("/books", methods=["GET"])
def get_books():
    """
    Get all books
    ---
    responses:
      200:
        description: List of all books
    """

    books = get_all_books()

    return books, 200
@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):
    """
    Get a book by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the book
    responses:
      200:
        description: Book found successfully
      404:
        description: Book not found
    """
    book = get_book_by_id(id)
    if book is None:
        return {"message": "Book not found"}, 404

    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "price": book.price,
        "published_year": book.published_year,
        "created_at": book.created_at
    }, 200
    
    
@app.route("/books/<int:id>", methods=["PUT"])
def update_book(id):
    """
    Update a book
    ---
    consumes:
      - application/json
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the book

      - in: body
        name: book
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
            price:
              type: number
            published_year:
              type: integer

    responses:
      200:
        description: Book updated successfully
      404:
        description: Book not found
    """
    data = request.json
    book = update_book_service(id, data)


    if book is None:
        return {"message": "Book not found"}, 404

    return {
        "message": "Book updated successfully"
    }, 200


@app.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    """
    Delete a book
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the book

    responses:
      200:
        description: Book deleted successfully
      404:
        description: Book not found
    """

    
    book = delete_book_service(id)
    if book is None:
        return {"message": "Book not found"}, 404
    return {
        "message": "Book deleted successfully"
    }, 200

if __name__ == "__main__":
    app.run(debug=True)