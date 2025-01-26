import random

import pytest
from fastapi_pagination import set_params, Params
from starlette import status
from starlette.testclient import TestClient

from schemas import AuthorUpdate, AuthorCreate


@pytest.mark.parametrize("page_num, size, expected_count, page_count", [
    (1, 10, 10, 2),
    (2, 10, 2, 2),
    (1, 20, 12, 1),
    (2, 12, 0, 1)
])
def test_get_authors_paginated(page_num: int, size: int, expected_count: int, page_count: int, new_author, client: TestClient):
    """
    Тестируем получение авторов на тестовой базе с пагинацией
    Создаём 12 авторов и проверяем количество
    """
    # Arrange
    author_quantity = 12
    for i in range(author_quantity):
        new_author(f'Super_{i}', f'Man_{i}')
    set_params(Params(page=page_num, size=size))

    # Act
    response = client.get('/api/authors')
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(data['items']) == expected_count
    assert data['total'] == author_quantity
    assert data['page'] == page_num
    assert data['size'] == size
    assert data['pages'] == page_count


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


@pytest.mark.parametrize("page_num, size, expected_count, page_count", [
    (1, 10, 10, 2),
    (2, 10, 2, 2),
    (1, 20, 12, 1),
    (2, 12, 0, 1)
])
def test_get_author_books_paginated(page_num: int, size: int, expected_count: int, page_count: int, new_author, new_book, client: TestClient):
    """
    Тестируем пагинацию при получении книг автора
    Создаём автора, 12 книг для него и проверяем инфу
    """
    # Arrange
    author_1 = new_author('Super', 'Man')
    book_quantity = 12
    for i in range(book_quantity):
        new_book(title=f'Book_{i}', price=random.randint(1, 20), author_id=author_1.id)
    set_params(Params(page=page_num, size=size))

    # Act
    response = client.get(f'/api/authors/{author_1.id}/books')
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(data['items']) == expected_count
    assert data['total'] == book_quantity
    assert data['page'] == page_num
    assert data['size'] == size
    assert data['pages'] == page_count


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
