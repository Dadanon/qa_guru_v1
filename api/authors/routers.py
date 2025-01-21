from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import status

from models import get_result
from schemas import AuthorListed, AuthorDetail
from . import crud
from database import get_db


router = APIRouter()


@router.get('', response_model=List[AuthorListed], status_code=status.HTTP_200_OK)
def get_authors(db: Session = Depends(get_db)):
    return get_result(db, crud.get_authors)


@router.get('/{author_id}', response_model=AuthorDetail, status_code=status.HTTP_200_OK)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    return get_result(db, crud.get_author_by_id, author_id)
