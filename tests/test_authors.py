import math

import pytest
from fastapi_pagination import set_params, Params
from starlette import status
from starlette.testclient import TestClient


# INFO: get authors pagination block -----------------------------------------------------------------------------------

@pytest.mark.parametrize("data_count, page_num, size", [
    (20, 1, 10),
    (16, 2, 10),
    (35, 1, 20),
    (11, 2, 12)
])
def test_check_get_authors_items_count_and_total(data_count: int, page_num: int, size: int, new_authors, client: TestClient):
    """Тестируем получение корректного количества объектов на данной странице и общего количества авторов в ответе"""
    # Arrange
    new_authors(data_count)
    set_params(Params(page=page_num, size=size))

    # Act
    response = client.get('/api/authors')
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    # Assert
    expected_count: int = max(0, min(size, data_count - (page_num - 1) * size))  # Ожидаемое количество объектов в ответе
    assert len(data['items']) == expected_count
    assert data['total'] == data_count


@pytest.mark.parametrize("data_count, size", [
    (27, 10),
    (13, 10),
    (35, 14),
    (11, 12)
])
def test_check_get_authors_page_count(data_count: int, size: int, new_authors, client: TestClient):
    """Тестируем получение корректного количества страниц в ответе, страница всегда первая"""
    # Arrange
    new_authors(data_count)
    set_params(Params(page=1, size=size))

    # Act
    response = client.get('/api/authors')
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    # Assert
    expected_page_count: int = math.ceil(data_count / size)  # Ожидаемое количество страниц в ответе
    assert data['pages'] == expected_page_count


@pytest.mark.parametrize("data_count, size", [
    (20, 10),
    (16, 10),
    (35, 20),
    (73, 15)
])
def test_check_get_authors_different_data_on_different_pages(data_count: int, size: int, new_authors,
                                                             client: TestClient):
    """Тестируем получение разных данных об авторах на 1 и 2 страницах.
    Хардкод тут в том, что мы нарочито выставляем в параметрах
    количество данных больше размера страницы для того, чтобы
    на второй странице гарантированно были данные"""
    # Arrange
    new_authors(data_count)
    set_params(Params(page=1, size=size))

    # Act
    response_first = client.get('/api/authors')
    assert response_first.status_code == status.HTTP_200_OK

    data_first = response_first.json()

    set_params(Params(page=2, size=size))
    response_second = client.get('/api/authors?page=2')
    assert response_second.status_code == status.HTTP_200_OK

    data_second = response_second.json()

    # Assert
    # Проверим в ответе следующие параметры, которые должны отличаться: номер страницы, айди и полное имя первого автора на странице
    assert data_first['page'] != data_second['page']
    assert data_first['items'][0]['id'] != data_second['items'][0]['id']
    assert data_first['items'][0]['full_name'] != data_second['items'][0]['full_name']


# INFO: end block ------------------------------------------------------------------------------------------------------

# INFO: get author books pagination block ------------------------------------------------------------------------------

@pytest.mark.parametrize("data_count, page_num, size", [
    (20, 1, 10),
    (16, 2, 10),
    (35, 1, 20),
    (11, 2, 12)
])
def test_check_get_author_books_items_count(data_count: int, page_num: int, size: int, new_books, client: TestClient):
    """Тестируем получение корректного количества объектов на данной странице и общего количества книг автора в ответе"""
    # Arrange
    author_id: int = new_books(data_count)
    set_params(Params(page=page_num, size=size))

    # Act
    response = client.get(f'/api/authors/{author_id}/books')
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    # Assert
    expected_count: int = max(0, min(size, data_count - (page_num - 1) * size))  # Ожидаемое количество объектов в ответе
    assert len(data['items']) == expected_count
    assert data['total'] == data_count


@pytest.mark.parametrize("data_count, size", [
    (27, 10),
    (13, 10),
    (35, 14),
    (11, 12)
])
def test_check_get_author_books_page_count(data_count: int, size: int, new_books, client: TestClient):
    """Тестируем получение корректного количества книг автора в ответе, страница всегда первая"""
    # Arrange
    author_id: int = new_books(data_count)
    set_params(Params(page=1, size=size))

    # Act
    response = client.get(f'/api/authors/{author_id}/books')
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    # Assert
    expected_page_count: int = math.ceil(data_count / size)  # Ожидаемое количество страниц в ответе
    assert data['pages'] == expected_page_count


@pytest.mark.parametrize("data_count, size", [
    (20, 10),
    (16, 10),
    (35, 20),
    (73, 15)
])
def test_check_get_author_books_different_data_on_different_pages(data_count: int, size: int, new_books,
                                                                  client: TestClient):
    """Тестируем получение разных данных о книгах автора на 1 и 2 страницах.
    Хардкод тут в том, что мы нарочито выставляем в параметрах
    количество данных больше размера страницы для того, чтобы
    на второй странице гарантированно были данные"""
    # Arrange
    author_id: int = new_books(data_count)
    set_params(Params(page=1, size=size))

    # Act
    response_first = client.get(f'/api/authors/{author_id}/books')
    assert response_first.status_code == status.HTTP_200_OK

    data_first = response_first.json()

    set_params(Params(page=2, size=size))
    response_second = client.get(f'/api/authors/{author_id}/books')
    assert response_second.status_code == status.HTTP_200_OK

    data_second = response_second.json()

    # Assert
    # Проверим в ответе следующие параметры, которые должны отличаться: номер страницы, айди и название книги на странице
    assert data_first['page'] != data_second['page']
    assert data_first['items'][0]['id'] != data_second['items'][0]['id']
    assert data_first['items'][0]['title'] != data_second['items'][0]['title']


# INFO: end block ------------------------------------------------------------------------------------------------------
