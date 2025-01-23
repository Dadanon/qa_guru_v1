import os

import dotenv
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient


@pytest.mark.smoke
def test_ping(client: TestClient):
    # Act
    response = client.get(f'/api/smoke/ping')
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert data == 'pong'


@pytest.mark.smoke
def test_envs():
    dotenv.load_dotenv()
    assert os.getenv('DATABASE_URL') is not None


@pytest.fixture(scope="module", name='db_connection')
def db_connection():
    dotenv.load_dotenv()
    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)
    with Session(engine) as connection:
        yield connection


@pytest.mark.smoke
def test_db_access(db_connection):
    # Act
    result = db_connection.execute(text("SELECT 1"))

    # Assert
    assert db_connection is not None
    assert result.scalar() == 1
