import datetime

import pytest
import requests
from pydantic import ValidationError
from starlette import status

from schemas_reqres import *


ROOT_URL = 'https://reqres.in/api/'
USERS_ON_PAGE = 6
TOTAL_USERS = 12
RESOURCES_ON_PAGE = USERS_ON_PAGE
TOTAL_RESOURCES = TOTAL_USERS
FAILED_USER_ID = 33
FAILED_RESOURCE_ID = FAILED_USER_ID
DEFAULT_PAGE_NUMBER_WITH_DELAY = 1


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


def test_list_users_empty():
    """Тест успешного получения пустого списка пользователей на несуществующей странице"""
    # Arrange
    empty_page_number = 3
    url = f'{ROOT_URL}users?page={empty_page_number}'
    # Act
    response = requests.get(url)
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK

    assert 'data' in data
    assert len(data['data']) == 0

    assert 'support' in data


@pytest.mark.parametrize("user_id, email", [(1, 'george.bluth@reqres.in'), (2, 'janet.weaver@reqres.in')])
def test_single_user_success(user_id: int, email: str):
    """Проверим получение одиночного существующего пользователя"""
    # Arrange
    url = f'{ROOT_URL}users/{user_id}'
    # Act
    response = requests.get(url)
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK

    assert 'data' in data
    assert data['data']['id'] == user_id
    assert data['data']['email'] == email
    # Проверим конкретного пользователя
    try:
        User.model_validate(data['data'])
    except ValidationError as e:
        pytest.fail(f'Single user validation error, {e}')

    assert 'support' in data

    # Проверим структуру спама
    try:
        Support.model_validate(data['support'])
    except ValidationError as e:
        pytest.fail(f'Support validation error, {e}')


def test_single_user_error():
    """Проверим получение одиночного несуществующего пользователя"""
    # Arrange
    url = f'{ROOT_URL}users/{FAILED_USER_ID}'
    # Act
    response = requests.get(url)
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data == {}


@pytest.mark.parametrize("page", [1, 2])
def test_list_resources_success(page: int):
    """Тест успешного получения списка ресурсов на существующих страницах"""
    # Arrange
    url = f'{ROOT_URL}unknown?page={page}'
    # Act
    response = requests.get(url)
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK

    assert 'page' in data
    assert data['page'] == page

    assert 'per_page' in data
    assert data['per_page'] == RESOURCES_ON_PAGE

    assert 'total' in data
    assert data['total'] == TOTAL_RESOURCES

    assert 'total_pages' in data
    assert data['total_pages'] == TOTAL_RESOURCES / RESOURCES_ON_PAGE

    assert 'data' in data
    assert len(data['data']) == RESOURCES_ON_PAGE

    # Проверим какой-нибудь ресурс
    try:
        Resource.model_validate(data['data'][0])
    except ValidationError as e:
        pytest.fail(f'Resource validation error, {e}')

    assert 'support' in data

    # Проверим структуру спама
    try:
        Support.model_validate(data['support'])
    except ValidationError as e:
        pytest.fail(f'Support validation error, {e}')


def test_list_resources_empty():
    """Тест успешного получения пустого списка ресурсов на несуществующей странице"""
    # Arrange
    empty_page_number = 3
    url = f'{ROOT_URL}unknown?page={empty_page_number}'
    # Act
    response = requests.get(url)
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK

    assert 'data' in data
    assert len(data['data']) == 0

    assert 'support' in data


@pytest.mark.parametrize("resource_id, name", [(1, 'cerulean'), (2, 'fuchsia rose')])
def test_single_resource_success(resource_id: int, name: str):
    """Проверим получение одиночного существующего ресурса"""
    # Arrange
    url = f'{ROOT_URL}unknown/{resource_id}'
    # Act
    response = requests.get(url)
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK

    assert 'data' in data
    assert data['data']['id'] == resource_id
    assert data['data']['name'] == name
    # Проверим конкретного пользователя
    try:
        Resource.model_validate(data['data'])
    except ValidationError as e:
        pytest.fail(f'Single resource validation error, {e}')

    assert 'support' in data

    # Проверим структуру спама
    try:
        Support.model_validate(data['support'])
    except ValidationError as e:
        pytest.fail(f'Support validation error, {e}')


def test_single_resource_error():
    """Проверим получение одиночного несуществующего ресурса"""
    # Arrange
    failed_resource_id = 33
    url = f'{ROOT_URL}unknown/{FAILED_RESOURCE_ID}'
    # Act
    response = requests.get(url)
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data == {}


def test_create_user_success():
    """Проверим создание пользователя"""
    # Arrange
    user_create_form: UserCreate = UserCreate(name='Leader', job='Prisoner')
    url = f'{ROOT_URL}users'

    # Act
    response = requests.post(url, json=user_create_form.model_dump())
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_201_CREATED

    # Проверим форму ответа
    try:
        UserCreateResponse.model_validate(data)
    except ValidationError as e:
        pytest.fail(f'User create response form validation error, {e}')

    assert data['name'] == user_create_form.name
    assert data['job'] == user_create_form.job


@pytest.mark.parametrize("user_id, name, job", [(1, 'New leader', 'Collector'), (2, 'Extra virgin', 'Crashdropper')])
def test_update_user_success(user_id: int, name: str, job: str):
    """Проверим изменение пользователя (UPDATE)"""
    # Arrange
    user_update_form: UserUpdate = UserUpdate(name=name, job=job)
    url = f'{ROOT_URL}users/{user_id}'

    # Act
    response = requests.put(url, json=user_update_form.model_dump())
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK

    # Проверим форму ответа
    try:
        UserUpdateResponse.model_validate(data)
    except ValidationError as e:
        pytest.fail(f'User update response form validation error, {e}')

    assert data['name'] == user_update_form.name
    assert data['job'] == user_update_form.job


@pytest.mark.parametrize("user_id, name, job", [(1, 'New leader', 'Collector'), (2, 'Extra virgin', 'Crashdropper')])
def test_patch_user_success(user_id: int, name: str, job: str):
    """Проверим изменение пользователя (PATCH)"""
    # Arrange
    user_patch_form: UserPatch = UserPatch(name=name, job=job)
    url = f'{ROOT_URL}users/{user_id}'

    # Act
    response = requests.patch(url, json=user_patch_form.model_dump())
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK

    # Проверим форму ответа
    try:
        UserPatchResponse.model_validate(data)
    except ValidationError as e:
        pytest.fail(f'User patch response form validation error, {e}')

    assert data['name'] == user_patch_form.name
    assert data['job'] == user_patch_form.job


@pytest.mark.parametrize("user_id", [1, 2])
def test_delete_user_success(user_id: int):
    """Проверим удаление существующего пользователя"""
    # Arrange
    url = f'{ROOT_URL}users/{user_id}'

    # Act
    response = requests.delete(url)
    response_text: str = response.text

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response_text == ''


@pytest.mark.parametrize("user_id", [15, 26])
def test_delete_user_error(user_id: int):
    """Проверим удаление несуществующего пользователя"""
    # Arrange
    url = f'{ROOT_URL}users/{user_id}'

    # Act
    response = requests.delete(url)
    response_text: str = response.text

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT  # INFO: удаление несуществующего пользователя не должно давать ту же ошибку


@pytest.mark.parametrize("email, password", [('eve.holt@reqres.in', 'pistol')])
def test_register_success(email: str, password: str):
    """Проверим успешную регистрацию"""
    # Arrange
    register_form: RegisterForm = RegisterForm(email=email, password=password)
    url = f'{ROOT_URL}register'

    # Act
    response = requests.post(url, json=register_form.model_dump())
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK

    # Проверим структуру ответа
    try:
        RegisterResponseSuccess.model_validate(data)
    except ValidationError as e:
        pytest.fail(f'Register response form validation error, {e}')


@pytest.mark.parametrize("password", ['the_best_password'])
def test_register_error_missing_email(password: str):
    """Проверим ошибочную регистрацию при отсутствии email"""
    # Arrange
    url = f'{ROOT_URL}register'

    # Act
    response = requests.post(url, data={'password': password})
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in data
    assert data['error'] == 'Missing email or username'  # INFO: username не указывается в форме, почему он присутствует в описании ошибки?


@pytest.mark.parametrize("email", ['superuser@megaboy.girl'])
def test_register_error_missing_password(email: str):
    """Проверим ошибочную регистрацию при отсутствии password"""
    # Arrange
    url = f'{ROOT_URL}register'

    # Act
    response = requests.post(url, data={'email': email})
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in data
    assert data['error'] == 'Missing password'


@pytest.mark.parametrize("email, password", [('eve.holt@reqres.in', 'cityslicka'), ('michael.lawson@reqres.in', 'michaelPass')])
def test_login_success(email: str, password: str):
    """Проверим успешную авторизацию"""
    # Arrange
    login_form: LoginForm = LoginForm(email=email, password=password)
    url = f'{ROOT_URL}login'

    # Act
    response = requests.post(url, json=login_form.model_dump())
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK

    # Проверим структуру ответа
    try:
        LoginResponseSuccess.model_validate(data)
    except ValidationError as e:
        pytest.fail(f'Login response form validation error, {e}')


@pytest.mark.parametrize("password", ['the_best_password'])
def test_login_error_missing_email(password: str):
    """Проверим ошибочную авторизацию при отсутствии email"""
    # Arrange
    url = f'{ROOT_URL}login'

    # Act
    response = requests.post(url, data={'password': password})
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in data
    assert data['error'] == 'Missing email or username'  # INFO: username не указывается в форме, почему он присутствует в описании ошибки?


@pytest.mark.parametrize("email", ['superuser@megaboy.girl'])
def test_login_error_missing_password(email: str):
    """Проверим ошибочную авторизацию при отсутствии password"""
    # Arrange
    url = f'{ROOT_URL}login'

    # Act
    response = requests.post(url, data={'email': email})
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in data
    assert data['error'] == 'Missing password'


@pytest.mark.parametrize("delay", [1, 3])
def test_list_users_delay_success(delay: int):
    """Тест успешного получения списка пользователей на 1 странице при определённой задержке"""
    # Arrange
    url = f'{ROOT_URL}users?delay={delay}'
    # Act
    start_time: datetime = datetime.now()
    response = requests.get(url)
    end_time: datetime = datetime.now()  # Предположим что апм запрос выполняется мгновенно, тогда проверим что дельта получения запроса больше указанного delay
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK

    assert 'page' in data
    assert data['page'] == DEFAULT_PAGE_NUMBER_WITH_DELAY

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

    # Проверим задержку
    api_delay: int = (end_time - start_time).seconds
    assert api_delay >= delay
