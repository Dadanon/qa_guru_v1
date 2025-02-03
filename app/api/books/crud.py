from sqlmodel import Session

from app.models.models import Book, BookBase


def create_book(db: Session, book: BookBase) -> Book:
    new_book: Book = Book.model_validate(book)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book
