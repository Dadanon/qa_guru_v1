from typing import Optional

from sqlalchemy import and_

from schemas import BookListed, BookDetail, BookUpdate, BookCreate
from models import *


def get_books(db: Session) -> List[BookListed]:
    db_books: List[Book] = db.query(Book).all()
    return [BookListed.model_validate(book) for book in db_books]


def get_book_by_id(db: Session, book_id: int) -> BookDetail:
    db_book: Optional[Book] = db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail=f'Book not found by id: {book_id}')
    return BookDetail.model_validate(db_book)


def update_book(db: Session, book_id: int, form: BookUpdate) -> BookDetail:
    db_book: Optional[Book] = db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail=f'Book not found by id: {book_id}')
    if form.title:
        db_book.title = form.title
    if form.price:
        db_book.price = form.price
    db.add(db_book)
    db.commit()
    return BookDetail.model_validate(db_book)


def create_book(db: Session, form: BookCreate) -> BookDetail:
    # Проверим, есть ли автора с таким id
    check_model(db, Author, form.author_id)
    # У автора не может быть 2 книг с одинаковым названием, он же не Донцова
    duplicate_exists: bool = db.query(exists().where(and_(Book.title == form.title, Book.author_id == form.author_id))).scalar()
    if duplicate_exists:
        raise HTTPException(status_code=400, detail=f'У автора с id {form.author_id} уже есть книга с названием {form.title}')
    new_book: Book = Book(title=form.title, price=form.price, author_id=form.author_id)
    db.add(new_book)
    db.commit()
    return BookDetail.model_validate(new_book)


def delete_book(db: Session, book_id: int) -> int:
    """Возвращаем id книги после её удаления для фильтрации списка книг например"""
    db_book: Optional[Book] = db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail=f'Book not found by id: {book_id} and cannot be deleted')
    db.delete(db_book)
    db.commit()
    return book_id
