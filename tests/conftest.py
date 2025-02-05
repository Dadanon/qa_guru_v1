import time
from typing import Type

import pytest
from dotenv import load_dotenv
from faker import Faker
from pydantic import BaseModel
from pydantic_core import ValidationError
from sqlalchemy import StaticPool
from sqlmodel import create_engine, SQLModel, Session
from starlette.testclient import TestClient

from app.models.database import get_db
from app.main import app
from app.models.models import Author, AuthorBase

load_dotenv('.env')


@pytest.fixture
def faker():
    faker = Faker()
    faker.seed_instance(int(time.time()))
    return faker


def validate_model(model: Type[BaseModel], validator: Type[BaseModel]):
    try:
        validator.model_validate(model)
    except ValidationError:
        raise AssertionError(f'Invalid model: {model.__name__}')


@pytest.fixture
def session():
    """Делаем тесты на любой базе, выбираем sqlite"""
    sqlmodel_database_url = 'sqlite://'
    engine = create_engine(sqlmodel_database_url, connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def new_author(session: Session, faker):
    """Создаём нового автора"""

    def _new_author():
        author: Author = Author(first_name=faker.first_name(), last_name=faker.last_name())
        session.add(author)
        session.commit()
        session.refresh(author)
        return author

    yield _new_author


@pytest.fixture
def new_author_data(faker):
    """Создаём тестовые данные для создания и изменения пользователя"""
    def _new_author_data():
        author_data: AuthorBase = AuthorBase(first_name=faker.first_name(), last_name=faker.last_name())
        return author_data
    yield _new_author_data
