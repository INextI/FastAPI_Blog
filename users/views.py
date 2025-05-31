from fastapi import APIRouter, Depends, HTTPException,status, Form
from .shemas import UserBase, UserBaseFull, UserCreate, Token
from core.models import User
from core.models import db_helper
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from auth.utils import create_access_token
from auth.security import verify_password

router = APIRouter(prefix='/users', tags=["User"])

@router.post('/', response_model= UserBaseFull)
async def create_user(user: UserCreate,
                      session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
                      ):
    
    return await crud.create_user(user_in= user, session= session)

@router.get('/', response_model=list[UserBaseFull])
async def get_users(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    return await crud.get_users(session= session)

@router.post('/register', response_model=Token)
async def registr_user(user_in: UserCreate,
                       session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                       ):
    existing = await crud.get_user_by_email(email=user_in.email, session=session)

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exsist!")
    
    user = await crud.create_user(user_in=user_in, session=session)

    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}


@router.post('/login', response_model=Token)
async def login_user(
                     session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                     email: Annotated[str, Form()],
                     password: Annotated[str, Form()],
                     ):
    user = await crud.get_user_by_email(email=email, session=session)

    if not user or not verify_password(plain=password, hashed=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}

    

