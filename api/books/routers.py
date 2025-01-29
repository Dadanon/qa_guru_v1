from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from sqlalchemy.orm import Session
from fastapi import status

from models import get_result
from schemas import BookListed
from . import crud
from database import get_db


router = APIRouter(prefix="/api/books", tags=["Books"])


@router.get('', response_model=Page[BookListed], status_code=status.HTTP_200_OK)
def get_books(db: Session = Depends(get_db)):
    disable_installed_extensions_check()
    return paginate(get_result(db, crud.get_books))
