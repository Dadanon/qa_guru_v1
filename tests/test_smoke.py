import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv(".env")


@pytest.mark.smoke
def test_docker_database_url_availability():
    # Act
    sqlmodel_database_url = os.getenv("DOCKER_DATABASE_URL")

    # Assert
    assert sqlmodel_database_url is not None


@pytest.mark.smoke
def test_db_availability(session):
    # Act
    response = session.exec(text("SELECT 1;"))

    # Assert
    assert response is not None
