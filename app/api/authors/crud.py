from fastapi import HTTPException
from starlette import status

from app.models.models import Session, AuthorBase, AuthorDetail
from app.models.models import Author


def get_author(db: Session, author_id: int) -> AuthorDetail:
    db_author: Author | None = db.get(Author, author_id)
    if not db_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Author not found')
    return AuthorDetail.model_validate(db_author)


def create_author(db: Session, author: AuthorBase) -> Author:
    new_author: Author = Author.model_validate(author)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def delete_author(db: Session, author_id: int) -> int:
    """Возвращаем id удаленного автора, например, для фильтрации списка авторов или проверки, что автор отсутствует в БД после удаления"""
    db_author: Author | None = db.get(Author, author_id)
    if not db_author:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Cannot delete author that does not exist')
    db.delete(db_author)
    db.commit()
    return db_author.id


def update_author(db: Session, author_id: int, author: AuthorBase) -> Author:
    db_author: Author | None = db.get(Author, author_id)
    if not db_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Author not found')
    author_data = author.model_dump(exclude_unset=True)
    db_author.sqlmodel_update(author_data)
    db.commit()
    db.refresh(db_author)
    return db_author
