from starlette import status

from app.models.models import Author
from tests.conftest import validate_model


def test_get_author(new_author, client):
    # Arrange
    db_author = new_author()

    # Act
    response = client.get(f'/api/authors/{db_author.id}')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Assert
    validate_model(data, Author)
    assert data['id'] == db_author.id
    assert data['first_name'] == db_author.first_name
    assert data['last_name'] == db_author.last_name


def test_create_author(new_author_data, client):
    # Arrange
    author_create_data = new_author_data()

    # Act
    response = client.post(f'/api/authors', json=author_create_data.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    # Assert
    validate_model(data, Author)
    assert data['first_name'] == author_create_data.first_name
    assert data['last_name'] == author_create_data.last_name


def test_delete_author(new_author, client):
    # Arrange
    db_author = new_author()

    # Act
    response = client.delete(f'/api/authors/{db_author.id}')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Act
    assert isinstance(data, int)
    assert data == db_author.id


def test_update_author(new_author, new_author_data, client):
    # Arrange
    db_author = new_author()
    author_update_data = new_author_data()
    print(f'db_author: {db_author.model_dump()}, author_update_data: {author_update_data.model_dump()}')

    # Act
    response = client.patch(f'/api/authors/{db_author.id}', json=author_update_data.model_dump())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Act
    validate_model(data, Author)
    assert data['id'] == db_author.id
    assert data['first_name'] == author_update_data.first_name
    assert data['last_name'] == author_update_data.last_name
