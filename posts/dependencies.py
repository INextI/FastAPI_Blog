from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Path, Depends
from typing import Annotated
from core.models import db_helper, Post
from . import crud

async def post_by_id(post_id: Annotated[int, Path], 
                     session: Annotated[AsyncSession, Depends(db_helper.session_getter)]) -> Post:
    post = await crud.get_post(post_id=post_id, session= session)

    if post is not None:
        return post
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post with this ID doesnt exsist')