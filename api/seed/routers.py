from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from models import get_result
from schemas import BaseResponse
from . import crud

router = APIRouter(prefix="/api/seed", tags=["Seed"])


@router.post('', response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
def create_seed(db: Session = Depends(get_db)):
    return get_result(db, crud.create_seed_data)
