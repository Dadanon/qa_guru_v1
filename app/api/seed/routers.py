from fastapi import APIRouter, Depends
from sqlmodel import Session
from starlette import status

from app.models.database import get_db
from app.models.models import get_result
from app.schemas import BaseResponse
from . import crud

router = APIRouter(prefix="/api/seed", tags=["Seed"])
