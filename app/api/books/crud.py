from app.schemas import BookListed
from app.models.models import *


def get_books(db: Session) -> List[BookListed]:
    db_books: List[Book] = db.query(Book).all()
    return [BookListed.model_validate(book) for book in db_books]
