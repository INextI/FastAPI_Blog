from .schemas import PostCreate, PostRead, Post as PS, PostUpdate, PostUpdatePartial
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from  core.models import Post
from fastapi import HTTPException
from sqlalchemy import select



async def create_post(post_in: PostCreate, session: AsyncSession) -> Post:
    post = Post(**post_in.model_dump())
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

async def get_posts(session: AsyncSession) -> Post:
    stmt = select(Post).order_by(Post.id)
    result: Result = await session.execute(stmt)
    posts = result.scalars().all()
    return posts

async def delete_post(post_id: int, session: AsyncSession) -> None:
    stmt = select(Post).filter(Post.id == post_id)
    result: Result = await session.execute(stmt)
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="Post with this ID doesnt exsist")
    await session.delete(post)
    await session.commit()

async def get_post(post_id: int, session: AsyncSession) -> Post | None:
    return await session.get(Post, post_id)

async def update_post(post_update: PostUpdate, session: AsyncSession, post: Post) -> Post:
    for name, value in post_update.model_dump(exclude_unset=False).items():
        setattr(post, name, value)
    await session.commit()
    await session.refresh(post)
    return post

async def update_post_partial(post_update: PostUpdatePartial, session: AsyncSession, post: Post) -> Post:
    for name, value in post_update.model_dump(exclude_unset=True).items():
        setattr(post, name, value)
    await session.commit()
    await session.refresh(post)
    return post

