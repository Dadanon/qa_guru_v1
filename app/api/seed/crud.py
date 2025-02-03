import random

from sqlmodel import Session

from app.models.models import Author, Book
from app.schemas import BaseResponse

SEED_LENGTH = 12
"""Длина сид данных"""


def create_seed_data(db: Session) -> BaseResponse:
    """
    Создаем данные для просмотра: 12 авторов и 12 книг, только если данных еще нет
    """
    if not db.query(Author).limit(1).all():
        for i in range(SEED_LENGTH):
            author: Author = Author(first_name=f'author{i}', last_name=f'Super{i}')
            db.add(author)
            book: Book = Book(title=f'Book{i}', price=random.randint(2, 20), author=author)
            db.add(book)

        db.commit()
    return BaseResponse(detail='Тестовые данные успешно созданы')
