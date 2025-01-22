from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import status

from models import get_result
from schemas import AuthorListed, AuthorDetail, BookList, AuthorUpdate, AuthorCreate
from . import crud
from database import get_db


router = APIRouter()


@router.get('', response_model=List[AuthorListed], status_code=status.HTTP_200_OK)
def get_authors(db: Session = Depends(get_db)):
    return get_result(db, crud.get_authors)


@router.get('/{author_id}', response_model=AuthorDetail, status_code=status.HTTP_200_OK)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    return get_result(db, crud.get_author_by_id, author_id)


@router.get('/{author_id}/books', response_model=BookList, status_code=status.HTTP_200_OK)
def get_author_books(author_id: int, db: Session = Depends(get_db)):
    return get_result(db, crud.get_author_books, author_id)


@router.put('/{author_id}', response_model=AuthorDetail, status_code=status.HTTP_200_OK)
def update_author(author_id: int, form: AuthorUpdate, db: Session = Depends(get_db)):
    return get_result(db, crud.update_author, author_id, form)


@router.post('', response_model=AuthorDetail, status_code=status.HTTP_201_CREATED)
def create_author(form: AuthorCreate, db: Session = Depends(get_db)):
    return get_result(db, crud.create_author, form)


@router.delete('/{author_id}', response_model=int, status_code=status.HTTP_200_OK)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    return get_result(db, crud.delete_author, author_id)
