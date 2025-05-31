from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .image import Image
    from .user import User

class NewPost(Base):
    title: Mapped[str]
    img_id: Mapped[int] = mapped_column(ForeignKey("images.id", ondelete="SET NULL"))
    text: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    image: Mapped["Image"] = relationship("Image", backref="posts", lazy="joined")
    author: Mapped["User"] = relationship("User", back_populates="posts")