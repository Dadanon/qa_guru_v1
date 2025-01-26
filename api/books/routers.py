from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from sqlalchemy.orm import Session
from fastapi import status

from models import get_result
from schemas import BookListed, BookDetail, BookUpdate, BookCreate
from . import crud
from database import get_db


router = APIRouter(prefix="/api/books", tags=["Books"])


@router.get('', response_model=Page[BookListed], status_code=status.HTTP_200_OK)
def get_books(db: Session = Depends(get_db)):
    disable_installed_extensions_check()
    return paginate(get_result(db, crud.get_books))


@router.get('/{book_id}', response_model=BookDetail, status_code=status.HTTP_200_OK)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    return get_result(db, crud.get_book_by_id, book_id)


@router.put('/{book_id}', response_model=BookDetail, status_code=status.HTTP_200_OK)
def update_book(book_id: int, form: BookUpdate, db: Session = Depends(get_db)):
    return get_result(db, crud.update_book, book_id, form)


@router.post('', response_model=BookDetail, status_code=status.HTTP_201_CREATED)
def create_book(form: BookCreate, db: Session = Depends(get_db)):
    return get_result(db, crud.create_book, form)


@router.delete('/{book_id}', response_model=int, status_code=status.HTTP_200_OK)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return get_result(db, crud.delete_book, book_id)
