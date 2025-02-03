from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.models.database import get_db
from app.models.models import Book, get_result, BookBase
from . import crud

router = APIRouter(prefix="/api/books", tags=["Books"])


@router.post('', response_model=Book)
def create_book(book: BookBase, db: Session = Depends(get_db)):
    return get_result(db, crud.create_book, book)
