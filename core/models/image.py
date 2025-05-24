from .base import Base
from sqlalchemy.orm import Mapped

class Image(Base):
    file_name: Mapped[str] 