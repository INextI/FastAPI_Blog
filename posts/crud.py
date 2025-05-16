from .schemas import PostCreate, PostRead
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select


async def create_post(post: PostCreate, session: AsyncSession) -> PostCreate:
    session.add(post)
    await session.commit()
    return post