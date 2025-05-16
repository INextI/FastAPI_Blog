from sqlalchemy.ext.asyncio import (AsyncSession, 
AsyncEngine, 
async_sessionmaker,
create_async_engine)
from typing import AsyncGenerator


class DataBaseHelper:
    def __init__(self, url, echo):
        self.engine: AsyncEngine = create_async_engine(url= url, echo = echo)
        self.session_maker: AsyncSession = async_sessionmaker(
            bind=self.engine,
            autoflush= False,
            autocommit = False,
        )

    def despose(self) -> None:
        await self.engine.dispose()