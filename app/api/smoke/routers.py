from fastapi import APIRouter
from starlette import status

router = APIRouter(prefix="/api/smoke", tags=["Smoke"])


"""
Что можно проверить с помощью smoke тестов в данном случае?
1. Базовый ответ от сервера ping-pong
2. Доступность переменных окружения
3. Доступность БД
"""


@router.get('/ping', response_model=str, status_code=status.HTTP_200_OK)
def get_pong():
    return 'pong'
