from starlette import status
from starlette.testclient import TestClient


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
