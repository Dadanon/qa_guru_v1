import random

import pytest
from fastapi_pagination import set_params, Params
from starlette import status
from starlette.testclient import TestClient

from schemas import BookUpdate, BookCreate


@pytest.mark.parametrize("page_num, size, expected_count, page_count", [
    (1, 10, 10, 2),
    (2, 10, 2, 2),
    (1, 20, 12, 1),
    (2, 12, 0, 1)
])
def test_get_books_paginated(page_num: int, size: int, expected_count: int, page_count: int, new_author, new_book, client: TestClient):
    """
    Тестируем пагинацию при получении общего количества книг
    Создаём 12 авторов, по 1 книге на каждого и тестируем инфу
    """
    # Arrange
    item_quantity = 12
    for i in range(item_quantity):
        author = new_author(f'Mega_{i}', f'Man_{i}')
        new_book(title=f'Book_{i}', price=random.randint(1, 20), author_id=author.id)
    set_params(Params(page=page_num, size=size))

    # Act
    response = client.get(f'/api/books')
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(data['items']) == expected_count
    assert data['total'] == item_quantity
    assert data['page'] == page_num
    assert data['size'] == size
    assert data['pages'] == page_count


def test_get_book(new_author, new_book, client: TestClient):
    """
    Тестируем получение подробной информации о книге на тестовой базе
    Создаём автора, книгу для него и проверяем инфу
    """
    # Arrange
    author_1 = new_author('Super', 'Man')
    book_1 = new_book('About all', 15.3, author_1.id)

    # Act
    response = client.get(f'/api/books/{book_1.id}')
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert data['id'] == book_1.id
    assert data['price'] == book_1.price
    assert data['author_name'] == author_1.full_name


def test_update_book(new_author, new_book, client: TestClient):
    """
    Тестируем изменение данных книги на тестовой базе
    Создаём автора, книгу для него, изменяем данные книги и проверяем инфу
    """
    # Arrange
    author_1 = new_author('Super', 'Man')
    book_1 = new_book('About all', 15.3, author_1.id)
    book_update_form: BookUpdate = BookUpdate(title='Nothing to say', price=22.2)

    # Act
    response = client.put(f'/api/books/{book_1.id}', json=book_update_form.model_dump())
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert data['id'] == book_1.id
    assert data['title'] == book_update_form.title
    assert data['price'] == book_update_form.price
    assert data['author_name'] == author_1.full_name


def test_create_book(new_author, new_book, client: TestClient):
    """
    Тестируем создание книги у имеющегося автора на тестовой базе
    Создаём автора, книгу и проверяем инфу
    """
    # Arrange
    author_1 = new_author('Super', 'Man')
    book_create_form: BookCreate = BookCreate(title='About all', price=15.3, author_id=author_1.id)

    # Act
    response = client.post(f'/api/books', json=book_create_form.model_dump())
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert data['title'] == book_create_form.title
    assert data['price'] == book_create_form.price
    assert data['author_name'] == author_1.full_name


def test_delete_book(new_author, new_book, client: TestClient):
    """
    Тестируем удаление книги на тестовой базе
    Создаём автора, книгу для него, удаляем книгу и проверяем инфу
    """
    # Arrange
    author_1 = new_author('Mega', 'Man')
    book_1 = new_book('About all', 15.3, author_1.id)

    # Act
    response = client.delete(f'/api/books/{book_1.id}')
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert data == book_1.id
