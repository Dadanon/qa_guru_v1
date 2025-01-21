from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, ForeignKey("tree_tags.id"), primary_key=True)

    tree_view: Mapped["TreeView"] = relationship(
        "TreeView",
        back_populates="view_tags"
    )