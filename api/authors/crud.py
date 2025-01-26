from typing import Optional

from schemas import AuthorListed, AuthorDetail, BookList, BookListed, AuthorUpdate, AuthorCreate
from models import *


def get_authors(db: Session) -> List[AuthorListed]:
    db_authors: List[Author] = db.query(Author).all()
    return [AuthorListed.model_validate(author) for author in db_authors]


def get_author_by_id(db: Session, author_id: int) -> AuthorDetail:
    db_author: Optional[Author] = db.get(Author, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail=f'Author not found by id: {author_id}')
    return AuthorDetail.model_validate(db_author)


def get_author_books(db: Session, author_id: int) -> List[BookListed]:
    check_model(db, Author, author_id)
    db_author_books: List[Book] = db.query(Book).filter_by(author_id=author_id).all()
    return [BookListed.model_validate(book) for book in db_author_books]


def update_author(db: Session, author_id: int, form: AuthorUpdate) -> AuthorDetail:
    db_author: Optional[Author] = db.get(Author, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail=f'Author not found by id: {author_id}')
    if form.first_name:
        db_author.first_name = form.first_name
    if form.last_name:
        db_author.last_name = form.last_name
    db.add(db_author)
    db.commit()
    return AuthorDetail.model_validate(db_author)


def create_author(db: Session, form: AuthorCreate) -> AuthorDetail:
    # Проверим, нет ли уже автора с таким именем
    potential_author: Optional[Author] = db.query(Author).filter_by(first_name=form.first_name, last_name=form.last_name).first()
    if potential_author:
        raise HTTPException(status_code=400, detail=f'Author with first name {form.first_name} and last name {form.last_name} already exists')
    new_author: Author = Author(first_name=form.first_name, last_name=form.last_name)
    db.add(new_author)
    db.commit()
    return AuthorDetail.model_validate(new_author)


def delete_author(db: Session, author_id: int) -> int:
    """Возвращаем id автора после его удаления для фильтрации списка авторов например"""
    db_author: Optional[Author] = db.get(Author, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail=f'Author not found by id: {author_id} and cannot be deleted')
    db.delete(db_author)
    db.commit()
    return author_id
