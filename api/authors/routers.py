from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import status
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check


from models import get_result
from schemas import AuthorListed, AuthorDetail, AuthorUpdate, AuthorCreate, BookListed
from . import crud
from database import get_db


router = APIRouter(prefix="/api/authors", tags=["Authors"])


@router.get('', response_model=Page[AuthorListed], status_code=status.HTTP_200_OK)
def get_authors(db: Session = Depends(get_db)):
    disable_installed_extensions_check()
    return paginate(get_result(db, crud.get_authors))


@router.get('/{author_id}/books', response_model=Page[BookListed], status_code=status.HTTP_200_OK)
def get_author_books(author_id: int, db: Session = Depends(get_db)):
    disable_installed_extensions_check()
    return paginate(get_result(db, crud.get_author_books, author_id))
