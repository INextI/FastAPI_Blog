from sqlalchemy.ext.asyncio import AsyncSession
from core.models import NewPost
from .schemas import NewPostBase, NewPostCreate
from sqlalchemy import select
from sqlalchemy.engine import Result

async def create_post(title: str,
                      img_id: int,
                      text: str,
                      session: AsyncSession,
                      ):
    post = NewPost(title= title, img_id = img_id, text=text)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

async def get_posts(session: AsyncSession):
    stmt = select(NewPost).order_by(NewPost.id)
    result: Result = await session.execute(stmt)
    posts = result.scalars().all()
    return posts