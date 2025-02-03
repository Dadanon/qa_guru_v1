from typing import List, Callable, TypeVar, Type

from fastapi import HTTPException
from pydantic import computed_field
from sqlalchemy import exists
from sqlmodel import Session, SQLModel, Field, Relationship


class DefaultBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True, index=True)


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


class AuthorBase(SQLModel):
    first_name: str = Field(max_length=100, nullable=False)
    last_name: str = Field(max_length=100, nullable=False)


class Author(DefaultBase, AuthorBase, table=True):
    __tablename__ = 'authors'

    books: List['Book'] = Relationship(
        back_populates='author',
        sa_relationship_kwargs={
            'cascade': 'all, delete-orphan',
        }
    )


class AuthorDetail(DefaultBase, AuthorBase):
    books: List['Book'] = Field(exclude=True)

    @computed_field(alias='books')
    @property
    def author_books(self) -> List[str]:
        return [book.title for book in self.books]


class BookBase(SQLModel):
    title: str = Field(max_length=100, nullable=False)
    price: float = Field(nullable=False, gt=0)
    author_id: int = Field(foreign_key='authors.id', nullable=False)


class Book(DefaultBase, BookBase, table=True):
    __tablename__ = 'books'

    author: 'Author' = Relationship(
        back_populates='books'
    )
