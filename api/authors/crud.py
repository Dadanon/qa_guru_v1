from typing import Optional

from schemas import AuthorListed, AuthorDetail
from models import *


def get_authors(db: Session) -> List[AuthorListed]:
    db_authors: List[Author] = db.query(Author).all()
    return [AuthorListed.model_validate(author) for author in db_authors]


def get_author_by_id(db: Session, id: int) -> AuthorDetail:
    db_author: Optional[Author] = db.get(Author, id)
    if db_author is None:
        raise HTTPException(status_code=404, detail=f'Author not found by id: {id}')
    return AuthorDetail.model_validate(db_author)
