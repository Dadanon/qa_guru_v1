import os

import pytest
from dotenv import load_dotenv

load_dotenv(".env")


@pytest.mark.smoke
def test_docker_database_url_availability():
    # Act
    sqlmodel_database_url = os.getenv("DOCKER_DATABASE_URL")

    # Assert
    assert sqlmodel_database_url is not None


@pytest.mark.smoke
def test_db_availability(session):
    ...
