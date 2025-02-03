from fastapi import HTTPException
from starlette import status

from app.models.models import Session, AuthorBase, AuthorDetail
from app.models.models import Author


def get_author(db: Session, author_id: int) -> AuthorDetail:
    db_author = db.get(Author, author_id)
    if not db_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Author not found')
    return AuthorDetail.model_validate(db_author)


def create_author(db: Session, author: AuthorBase) -> Author:
    new_author: Author = Author.model_validate(author)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author
