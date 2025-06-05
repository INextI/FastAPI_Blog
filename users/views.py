from fastapi import APIRouter, Depends, HTTPException,status, Form
from .shemas import UserBase, UserBaseFull, UserCreate
from core.models import User
from core.models import db_helper
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud


router = APIRouter(prefix='/users', tags=["User"])

@router.post('/', response_model= UserBaseFull)
async def create_user(user: UserCreate,
                      session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
                      ):
    
    return await crud.create_user(user_in= user, session= session)

@router.get('/', response_model=list[UserBaseFull])
async def get_users(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    return await crud.get_users(session= session)


@router.get('/{user_id}', response_model=UserBase)
async def get_user(user_id: int,
                   session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                   ):
    return await crud.get_user_by_id(user_id=user_id,session=session)