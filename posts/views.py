from fastapi.routing import Request, APIRouter
from .schemas import PostCreate, PostRead
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from core.models import db_helper
router = APIRouter('/post/', tags=['Posts'])

@router.get('/')
async def get_post(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]) -> PostRead:
    pass

@router.post('/')
async def create_post(post: PostCreate,
                      session: Annotated[AsyncSession, Depends(db_helper.session_getter)]) -> PostCreate:

    pass