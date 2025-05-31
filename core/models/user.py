from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .new_post import NewPost

class User(Base):
    nickname: Mapped[str] = mapped_column(unique=True)
    is_admin: Mapped[bool]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    posts: Mapped[list["NewPost"]] = relationship("NewPost", back_populates='author', cascade='all, delete-orphan')

