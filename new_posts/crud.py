from sqlalchemy.ext.asyncio import AsyncSession
from core.models import NewPost
from .schemas import NewPostBase, NewPostCreate
from sqlalchemy import select
from sqlalchemy.engine import Result
from images import crud as img_crud

async def create_post(title: str,
                      img_id: int,
                      text: str,
                      session: AsyncSession,
                      ) -> NewPost:
    post = NewPost(title= title, img_id = img_id, text=text)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

async def get_posts(session: AsyncSession) -> list[NewPost]:
    stmt = select(NewPost).order_by(NewPost.id)
    result: Result = await session.execute(stmt)
    posts = result.scalars().all()
    return posts

async def delete_post(post_id: int, session: AsyncSession) -> None:
    post = await session.get(NewPost, post_id)
    await img_crud.delete_image(img_id=post.img_id, session= session)
    await session.delete(post)
    await session.commit()
