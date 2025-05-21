from fastapi import APIRouter, status
from .schemas import PostCreate, PostRead, Post
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from core.models import db_helper
from . import crud
from typing import List

router = APIRouter(prefix='/post', tags=['Posts'])

@router.get('/', response_model=List[PostRead])
async def get_post(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]) -> Post:
    return await crud.get_posts(session=session)

@router.post('/')
async def create_post(post: PostCreate,
                      session: Annotated[AsyncSession, Depends(db_helper.session_getter)]) -> Post:
    
    return await crud.create_post(session=session, post_in=post)

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int,
                        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]) -> None:
    await crud.delete_post(post_id=post_id, session=session)