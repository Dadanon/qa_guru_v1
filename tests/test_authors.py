import pytest
from pydantic import ValidationError
from starlette import status
from starlette.testclient import TestClient

from schemas import AuthorDetail, AuthorUpdate, AuthorCreate


def test_get_authors(new_author, client: TestClient):
    """
    Тестируем получение авторов на тестовой базе
    Создаём 2 авторов и проверяем количество
    """
    # Arrange
    author_1 = new_author('Super', 'Man')
    author_2 = new_author('Aqua', 'Marine')

    # Act
    response = client.get('/api/authors')
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 2
    assert data[0]['id'] == author_1.id
    assert data[0]['full_name'] == author_1.full_name
    assert data[1]['full_name'] == author_2.full_name


def test_get_author(new_author, new_book, client: TestClient):
    """
    Тестируем получение подробной информации об авторе на тестовой базе
    Создаём автора, пару книг для него и проверяем инфу
    """
    # Arrange
    author_1 = new_author('Super', 'Man')
    book_1 = new_book('About all', 15.3, author_1.id)
    book_2 = new_book('Nothing to do', 173.2, author_1.id)

    # Act
    response = client.get(f'/api/authors/{author_1.id}')
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert data['id'] == author_1.id
    assert data['full_name'] == author_1.full_name
    assert len(data['books']) == 2
    assert data['books'][0] == book_1.title
    assert data['books'][1] == book_2.title


def test_get_author_books(new_author, new_book, client: TestClient):
    """
    Тестируем получение подробной информации о книгах автора на тестовой базе
    Создаём автора, пару книг для него и проверяем инфу
    """
    # Arrange
    author_1 = new_author('Super', 'Man')
    book_1 = new_book('About all', 15.3, author_1.id)
    book_2 = new_book('Nothing to do', 173.2, author_1.id)

    # Act
    response = client.get(f'/api/authors/{author_1.id}/books')
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert data['total'] == 2
    assert len(data['books']) == 2
    assert data['books'][0]['title'] == book_1.title
    assert data['books'][1]['title'] == book_2.title


def test_update_author(new_author, new_book, client: TestClient):
    """
    Тестируем изменение данных автора на тестовой базе
    Создаём автора, пару книг для него, изменяем данные автора и проверяем инфу
    """
    # Arrange
    author_1 = new_author('Super', 'Man')
    new_book('About all', 15.3, author_1.id)
    new_book('Nothing to do', 173.2, author_1.id)
    author_update_form: AuthorUpdate = AuthorUpdate(first_name='Mega')

    # Act
    response = client.put(f'/api/authors/{author_1.id}', json=author_update_form.model_dump())
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert data['id'] == author_1.id
    assert data['full_name'] == 'Mega Man'  # INFO: не очень литералами проверять, но пока лучше не придумал
    assert len(data['books']) == 2


def test_create_author(new_author, client: TestClient):
    """
    Тестируем создание автора на тестовой базе
    Создаём автора и проверяем инфу
    """
    # Arrange
    author_create_form: AuthorCreate = AuthorCreate(first_name='Mega', last_name='Man')

    # Act
    response = client.post(f'/api/authors', json=author_create_form.model_dump())
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert data['full_name'] == f'{author_create_form.first_name} {author_create_form.last_name}'
    assert len(data['books']) == 0


def test_delete_author(new_author, client: TestClient):
    """
    Тестируем удаление автора на тестовой базе
    Создаём автора, удаляем его и проверяем инфу
    """
    # Arrange
    author_1 = new_author('Mega', 'Man')

    # Act
    response = client.delete(f'/api/authors/{author_1.id}')
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert data == author_1.id
