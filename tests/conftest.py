import random
from typing import List

import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database import Base, get_db
from main import app
from models import Author, check_model, Book
from schemas import AuthorDetail, BookDetail


@pytest.fixture(name='session')
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="new_author")
def new_author_fixture(session: Session):
    """Создаём нового автора"""
    def _new_author(first_name: str, last_name: str):
        author = Author(first_name=first_name, last_name=last_name)
        session.add(author)

        session.commit()
        return AuthorDetail.model_validate(author)

    yield _new_author


@pytest.fixture(name="new_authors")
def new_authors_fixture(new_author):
    """Создаём некоторое количество новых авторов"""
    def _new_authors(author_quantity: int):
        if author_quantity <= 1:
            return []
        author_list: List[AuthorDetail] = []
        for i in range(author_quantity):
            author = new_author(first_name=f'Test_author_{i}', last_name=f'The_best_{i}')
            author_list.append(author)
        return author_list

    yield _new_authors


@pytest.fixture(name="new_book")
def new_book_fixture(session: Session):
    """Создаём новую книгу"""
    def _new_book(title: str, price: float, author_id: int):
        check_model(session, Author, author_id)
        book = Book(title=title, price=price, author_id=author_id)
        session.add(book)

        session.commit()
        return BookDetail.model_validate(book)

    yield _new_book


@pytest.fixture(name="new_books")
def new_books_fixture(new_book, new_author):
    """Создаём некоторое количество новых книг одного автора. Возвращаем id этого автора"""
    def _new_books(book_quantity: int):
        if book_quantity < 1:
            return []
        book_list: List[BookDetail] = []
        author = new_author(first_name='Test_author', last_name='The_best')
        for i in range(book_quantity):
            book = new_book(title=f'Test_book_{i}', price=random.randint(0, 20), author_id=author.id)
            book_list.append(book)
        return author.id

    yield _new_books
