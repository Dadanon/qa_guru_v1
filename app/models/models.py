from typing import List, Callable, TypeVar, Type

from fastapi import HTTPException
from sqlalchemy import Integer, ForeignKey, String, Float, exists
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlmodel import Session, SQLModel, Field

from .database import Base


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

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)

    books: Mapped[List['Book']] = relationship(
        'Book',
        back_populates='author',
        cascade='all, delete-orphan'
    )


class Book(DefaultBase, table=True):
    __tablename__ = 'books'

    title: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('authors.id'), nullable=False)

    author: Mapped['Author'] = relationship(
        'Author',
        back_populates='books'
    )
