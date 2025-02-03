from fastapi import APIRouter
from starlette import status

router = APIRouter(prefix="/api/smoke", tags=["Smoke"])
