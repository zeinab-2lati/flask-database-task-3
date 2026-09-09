from models import Book
from datetime import datetime
from extensions import db


def get_all_books():
    books = Book.query.all()

    books_list = []

    for book in books:
        books_list.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "price": book.price,
            "published_year": book.published_year,
            "created_at": book.created_at.isoformat()
        })

    return books_list
def get_book_by_id(id):
    return Book.query.get(id)

def add_book(data):
    book = Book(
        title=data["title"],
        author=data["author"],
        price=data["price"],
        published_year=data["published_year"],
        created_at=datetime.now()
    )

    db.session.add(book)
    db.session.commit()

    return book

def update_book(id, data):
    book = Book.query.get(id)

    if book is None:
        return None

    book.title = data["title"]
    book.author = data["author"]
    book.price = data["price"]
    book.published_year = data["published_year"]

    db.session.commit()

    return book

def delete_book(id):
    book = Book.query.get(id)

    if book is None:
        return None

    db.session.delete(book)
    db.session.commit()

    return book