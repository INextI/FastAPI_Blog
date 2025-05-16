from sqlalchemy.ext.asyncio import (AsyncSession, 
AsyncEngine, 
async_sessionmaker,
create_async_engine)
from typing import AsyncGenerator
from core.config import settings

class DatabaseHelper:
    def __init__(self, url, echo):
        self.engine: AsyncEngine = create_async_engine(url= url, echo = echo)
        self.session_maker: AsyncSession = async_sessionmaker(
            bind=self.engine,
            autoflush= False,
            autocommit = False,
        )

    async def despose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_maker() as session:
            yield session

db_helper = DatabaseHelper(url= settings.db.url, echo = settings.db.echo)
