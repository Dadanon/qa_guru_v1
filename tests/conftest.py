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
