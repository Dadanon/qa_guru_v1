from typing import Optional

from schemas import AuthorListed, AuthorDetail, BookList, BookListed, AuthorUpdate, AuthorCreate
from models import *


def get_authors(db: Session) -> List[AuthorListed]:
    db_authors: List[Author] = db.query(Author).all()
    return [AuthorListed.model_validate(author) for author in db_authors]


def get_author_books(db: Session, author_id: int) -> List[BookListed]:
    check_model(db, Author, author_id)
    db_author_books: List[Book] = db.query(Book).filter_by(author_id=author_id).all()
    return [BookListed.model_validate(book) for book in db_author_books]
