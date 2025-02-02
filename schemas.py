from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field


class Initial(BaseModel):
    """An initial schema that only implements model_config settings"""
    model_config = ConfigDict(from_attributes=True)


class AuthorListed(Initial):
    id: int
    first_name: str = Field(exclude=True)
    last_name: str = Field(exclude=True)

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class AuthorList(Initial):
    total: int
    authors: List[AuthorListed]


class BookListed(Initial):
    id: int
    title: str


class BookList(Initial):
    total: int
    books: List[BookListed]


class AuthorDetail(AuthorListed):
    books: List[BookListed] = Field(exclude=True)

    @computed_field(alias='books')
    @property
    def author_books(self) -> List[str]:
        return [book.title for book in self.books]


class BookDetail(BookListed):
    price: float
    author: AuthorListed = Field(exclude=True)

    @computed_field
    @property
    def author_name(self) -> str:
        return self.author.full_name


class BookUpdate(Initial):
    title: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None)


class AuthorUpdate(Initial):
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)


class AuthorCreate(Initial):
    first_name: str
    last_name: str


class BookCreate(Initial):
    title: str
    price: float
    author_id: int


class BaseResponse(Initial):
    detail: str
