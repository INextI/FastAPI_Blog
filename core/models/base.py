from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
    
    created_at: Mapped[datetime] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column()

