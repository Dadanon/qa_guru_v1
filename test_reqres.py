import pytest
import requests
from pydantic import ValidationError
from starlette import status

from schemas_reqres import *


ROOT_URL = 'https://reqres.in/api/'
USERS_ON_PAGE = 6
TOTAL_USERS = 12


@pytest.mark.parametrize("page", [1, 2])
def test_list_users_success(page: int):
    """Тест успешного получения списка пользователей на существующих страницах"""
    # Arrange
    url = f'{ROOT_URL}users?page={page}'
    # Act
    response = requests.get(url)
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK

    assert 'page' in data
    assert data['page'] == page

    assert 'per_page' in data
    assert data['per_page'] == USERS_ON_PAGE

    assert 'total' in data
    assert data['total'] == TOTAL_USERS

    assert 'total_pages' in data
    assert data['total_pages'] == TOTAL_USERS / USERS_ON_PAGE

    assert 'data' in data
    assert len(data['data']) == USERS_ON_PAGE

    # Проверим какого-нибудь пользователя
    try:
        User.model_validate(data['data'][0])
    except ValidationError as e:
        pytest.fail(f'User validation error, {e}')

    assert 'support' in data

    # Проверим структуру спама
    try:
        Support.model_validate(data['support'])
    except ValidationError as e:
        pytest.fail(f'Support validation error, {e}')
