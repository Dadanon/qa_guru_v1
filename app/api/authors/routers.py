from fastapi import APIRouter, Depends
from sqlmodel import Session


from . import crud
from app.models.database import get_db
from app.models.models import get_result, Author
from app.schemas import AuthorDetail

router = APIRouter(prefix="/api/authors", tags=["Authors"])


@router.get('/{author_id}', response_model=AuthorDetail)
def get_author(author_id: int, db: Session = Depends(get_db)):
    return get_result(db, crud.get_author, author_id)


@router.post('', response_model=Author)
def create_author(author: Author, db: Session = Depends(get_db)):
    return get_result(db, crud.create_author, author)
