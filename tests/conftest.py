import os
from typing import Type

import pytest
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_core import ValidationError
from sqlmodel import create_engine, SQLModel, Session
from starlette.testclient import TestClient

from app.models.database import get_db
from app.main import app
from app.models.models import Author


load_dotenv('.env')


def validate_model(model: Type[BaseModel], validator: Type[BaseModel]):
    try:
        validator.model_validate(model)
    except ValidationError:
        raise AssertionError(f'Invalid model: {model.__name__}')


@pytest.fixture
def session():
    """Делаем тесты на любой базе, выбираем sqlite"""
    sqlmodel_database_url = os.getenv("DOCKER_DATABASE_URL")
    engine = create_engine(sqlmodel_database_url)
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
