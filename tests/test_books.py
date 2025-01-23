from starlette import status
from starlette.testclient import TestClient

from schemas import BookUpdate, BookCreate


def test_get_books(new_author, new_book, client: TestClient):
    """
    Тестируем получение книг на тестовой базе
    Создаём 2 авторов, каждому создаём по 1 книге и проверяем количество
    """
    # Arrange
    author_1 = new_author('Super', 'Man')
    author_2 = new_author('Aqua', 'Marine')
    book_1 = new_book('About all', 15.3, author_1.id)
    book_2 = new_book('Nothing to do', 173.2, author_2.id)

    # Act
    response = client.get('/api/books')
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 2
    assert data[0]['id'] == book_1.id
    assert data[1]['id'] == book_2.id
    assert data[0]['title'] == book_1.title
    assert data[1]['title'] == book_2.title


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
