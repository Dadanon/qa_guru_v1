from typing import List, Callable, TypeVar, Type

from fastapi import HTTPException
from sqlalchemy import exists
from sqlmodel import Session, SQLModel, Field, Relationship


class DefaultBase(SQLModel, table=False):
    id: int | None = Field(default=None, primary_key=True)


S = TypeVar('S')
T = TypeVar('T', bound=DefaultBase)  # Return any DefaultBase-derived class


def check_model(db: Session, model_type: Type[T], model_id: int) -> None:
    model_exists = db.query(exists().where(model_type.id == model_id)).scalar()
    if not model_exists:
        raise HTTPException(status_code=404, detail=f'{model_type.__name__} not found by id {model_id}')


def get_result(db: Session, function: Callable[..., S], *args, **kwargs) -> S:
    try:
        result = function(db, *args, **kwargs)
        return result
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


class Author(DefaultBase, table=True):
    __tablename__ = 'authors'

    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)

    books: List['Book'] = Relationship(
        back_populates='author',
        cascade_delete=True
    )


class Book(DefaultBase, table=True):
    __tablename__ = 'books'

    title: str = Field(nullable=False)
    price: float = Field(nullable=False)
    author_id: int = Field(foreign_key='authors.id', nullable=False)

    author: 'Author' = Relationship(
        back_populates='books'
    )
