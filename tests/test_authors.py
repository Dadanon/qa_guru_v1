import requests
from starlette import status

from app.models.models import AuthorDetail
from tests.conftest import validate_model


def test_get_author(new_author):
    # Arrange
    author = new_author()

    # Act
    response = requests.get(f'/api/authors/{author.id}')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Assert
    validate_model(author, AuthorDetail)
    assert data['id'] == author.id
    assert data['first_name'] == author.first_name
    assert data['last_name'] == author.last_name

