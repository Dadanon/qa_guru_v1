from fastapi import HTTPException
from starlette import status

from app.schemas import AuthorListed, BookListed, AuthorDetail
from app.models.models import Session
from typing import List
from app.models.models import Author, Book, check_model


def get_author(db: Session, author_id: int) -> AuthorDetail:
    db_author = db.get(Author, author_id)
    if not db_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Author not found')
    return AuthorDetail.model_validate(db_author)


def get_authors(db: Session) -> List[AuthorListed]:
    db_authors: List[Author] = db.query(Author).all()
    return [AuthorListed.model_validate(author) for author in db_authors]


def get_author_books(db: Session, author_id: int) -> List[BookListed]:
    check_model(db, Author, author_id)
    db_author_books: List[Book] = db.query(Book).filter_by(author_id=author_id).all()
    return [BookListed.model_validate(book) for book in db_author_books]
