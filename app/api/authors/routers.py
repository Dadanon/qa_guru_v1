from fastapi import APIRouter, Depends
from sqlmodel import Session


from . import crud
from app.models.database import get_db
from app.models.models import get_result, Author, AuthorBase, AuthorDetail

router = APIRouter(prefix="/api/authors", tags=["Authors"])


@router.get('/{author_id}', response_model=AuthorDetail)
def get_author(author_id: int, db: Session = Depends(get_db)):
    return get_result(db, crud.get_author, author_id)


@router.post('', response_model=Author)
def create_author(author: AuthorBase, db: Session = Depends(get_db)):
    return get_result(db, crud.create_author, author)


@router.delete('/{author_id}', response_model=int)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    return get_result(db, crud.delete_author, author_id)


@router.patch('/{author_id}', response_model=Author)
def update_author(author_id: int, author: AuthorBase, db: Session = Depends(get_db)):
    return get_result(db, crud.update_author, author_id, author)
