from typing import List, Callable, TypeVar, Type

from fastapi import HTTPException
from sqlalchemy import Integer, ForeignKey, String, Float, exists
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from database import Base


S = TypeVar('S')
T = TypeVar('T', bound=Base)  # Return any Base-derived class


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


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)

    books: Mapped[List['Book']] = relationship(
        'Book',
        back_populates='author',
        cascade='all, delete-orphan'
    )


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('authors.id'), nullable=False)

    author: Mapped['Author'] = relationship(
        'Author',
        back_populates='books'
    )
