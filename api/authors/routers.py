from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import status
from fastapi_pagination import Page, paginate, set_params, Params


from models import get_result
from schemas import AuthorListed, AuthorDetail, AuthorUpdate, AuthorCreate, BookListed
from . import crud
from database import get_db


router = APIRouter(prefix="/api/authors", tags=["Authors"])


set_params(Params(page=1, size=10))


@router.get('', response_model=Page[AuthorListed], status_code=status.HTTP_200_OK)
def get_authors(db: Session = Depends(get_db)):
    return paginate(get_result(db, crud.get_authors))


@router.get('/{author_id}', response_model=AuthorDetail, status_code=status.HTTP_200_OK)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    return get_result(db, crud.get_author_by_id, author_id)


@router.get('/{author_id}/books', response_model=Page[BookListed], status_code=status.HTTP_200_OK)
def get_author_books(author_id: int, db: Session = Depends(get_db)):
    return paginate(get_result(db, crud.get_author_books, author_id))


@router.put('/{author_id}', response_model=AuthorDetail, status_code=status.HTTP_200_OK)
def update_author(author_id: int, form: AuthorUpdate, db: Session = Depends(get_db)):
    return get_result(db, crud.update_author, author_id, form)


@router.post('', response_model=AuthorDetail, status_code=status.HTTP_201_CREATED)
def create_author(form: AuthorCreate, db: Session = Depends(get_db)):
    return get_result(db, crud.create_author, form)


@router.delete('/{author_id}', response_model=int, status_code=status.HTTP_200_OK)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    return get_result(db, crud.delete_author, author_id)
