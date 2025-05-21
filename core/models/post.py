from .base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Post(Base):
    name: Mapped[str] # = mapped_column()
    img: Mapped[str] #= mapped_column()
    description: Mapped[str] #= mapped_column()