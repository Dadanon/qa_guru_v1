from fastapi import HTTPException
from starlette import status

from app.schemas import AuthorDetail
from app.models.models import Session
from app.models.models import Author


def get_author(db: Session, author_id: int) -> AuthorDetail:
    db_author = db.get(Author, author_id)
    if not db_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Author not found')
    return AuthorDetail.model_validate(db_author)


def create_author(db: Session, author: Author) -> Author:
    if author.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Cannot create author with provided id')
    db.add(author)
    db.commit()
    db.refresh(author)
    return author
