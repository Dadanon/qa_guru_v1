import pytest
from starlette import status
from starlette.testclient import TestClient

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
    create_response = client.post(f'/api/authors', json=author_create_data.model_dump())
    assert create_response.status_code == status.HTTP_201_CREATED
    create_data = create_response.json()

    # Assert
    validate_model(create_data, Author)
    assert create_data['first_name'] == author_create_data.first_name
    assert create_data['last_name'] == author_create_data.last_name

    # Act (after create)
    get_after_create_response = client.get(f'/api/authors/{create_data['id']}')
    assert get_after_create_response.status_code == status.HTTP_200_OK
    get_after_create_data = get_after_create_response.json()

    # Assert (after create)
    validate_model(get_after_create_data, Author)
    assert get_after_create_data['id'] == create_data['id']


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
    update_response = client.patch(f'/api/authors/{db_author.id}', json=author_update_data.model_dump())
    assert update_response.status_code == status.HTTP_200_OK
    update_data = update_response.json()

    # Act
    validate_model(update_data, Author)
    assert update_data['id'] == db_author.id
    assert update_data['first_name'] == author_update_data.first_name
    assert update_data['last_name'] == author_update_data.last_name

    # Act (after create)
    get_after_update_response = client.get(f'/api/authors/{update_data['id']}')
    assert get_after_update_response.status_code == status.HTTP_200_OK
    get_after_update_data = get_after_update_response.json()

    # Assert (after create)
    validate_model(get_after_update_data, Author)
    assert get_after_update_data['id'] == update_data['id']


@pytest.mark.parametrize('invalid_get_method_name', ['post'])
def test_get_author_invalid_method(invalid_get_method_name: str, client):
    """Тестируем только post, т.к. delete доступен по тому же роуту (будет 404 ошибка - юзер не найден для удаления) и patch доступен по тому же роуту (будет 422 ошибка - не прислана форма)"""
    # Arrange
    method = getattr(client, invalid_get_method_name)
    test_author_id: int = 1  # ID пользователя для проверки некорректного метода

    # Act
    response = method(f'/api/authors/{test_author_id}')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.parametrize('invalid_get_method_name', ['patch'])
def test_create_author_invalid_method(invalid_get_method_name: str, client, new_author_data):
    """Тестируем только patch, т.к. для get и delete будет ошибка TypeError, вызванная наличием формы в запросе"""
    # Arrange
    method = getattr(client, invalid_get_method_name)
    author_create_data = new_author_data()

    # Act
    response = method(f'/api/authors', json=author_create_data.model_dump())
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_delete_author_not_found(client):
    # Arrange
    nonexistent_author_id: int = 1

    # Act
    response = client.delete(f'/api/authors/{nonexistent_author_id}')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_patch_author_not_found(client, new_author_data):
    # Arrange
    author_data = new_author_data()
    nonexistent_author_id: int = 1

    # Act
    response = client.patch(f'/api/authors/{nonexistent_author_id}', json=author_data.model_dump())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_patch_author_unprocessable_entity(client, new_author, new_author_data, faker):
    # Arrange
    db_author = new_author()
    invalid_author_data = {'first_name': faker.first_name()}

    # Act
    response = client.patch(f'/api/authors/{db_author.id}', json=invalid_author_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_author_unprocessable_entity(client, new_author_data, faker):
    # Arrange
    invalid_author_data = {'first_name': faker.first_name()}

    # Act
    response = client.post('/api/authors', json=invalid_author_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
