from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import status

from models import get_result
from schemas import BookListed
from . import crud
from database import get_db


router = APIRouter()


@router.get('', response_model=List[BookListed], status_code=status.HTTP_200_OK)
def get_books(db: Session = Depends(get_db)):
    return get_result(db, crud.get_books)
