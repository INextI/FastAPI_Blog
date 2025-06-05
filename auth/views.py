
from fastapi import APIRouter, Depends, Form, HTTPException, status, Response, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.models import db_helper
from users.shemas import UserCreate
from .shemas import Token
from users.shemas import UserBaseFull, UserMe
from users import crud
from .security import hash_password, validate_password
from .utils import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
)
from .cookie import SetTokenCookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix='/auth', tags=['JWT'])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login-test")

@router.post('/register', response_model=Token)
async def registr_user(user_in: UserCreate,
                       session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                       response: Response,
                       ):
    existing = await crud.get_user_by_email(email=user_in.email, session=session)

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exsist!")
    
    user = await crud.create_user(user_in=user_in, session=session)

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    SetTokenCookie(token=refresh_token).create_response(response=response)

    return {
        "access_token": access_token,
        }


@router.post('/login', response_model=Token)
async def login_user(
                     session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                     email: Annotated[str, Form()],
                     password: Annotated[str, Form()],
                     ):
    user = await crud.get_user_by_email(email=email, session=session)

    if not user or not validate_password(password=password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token" : refresh_token,
        }

    

@router.post('/refresh', response_model=Token, response_model_exclude_none=True)
async def refresh_token(request: Request): #refresh_token: Annotated[str, Form()]
    try:
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise HTTPException(status_code=401, detail="No refresh token cookie")

        payload = decode_refresh_token(refresh_token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid token payload")
        
        new_access_token = create_access_token({"sub": user_id})
        #new_refresh_token = create_refresh_token({"sub": user_id})

        return {
            "access_token" : new_access_token,
               }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    

@router.get('/me', response_model=UserMe)
async def get_token_info(token: Annotated[str, Depends(oauth2_scheme)],
                         session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
                         ):
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401)
    user = await crud.get_user_by_id(user_id=int(user_id), session=session)
    return user


@router.post('/login-test', response_model=Token, response_model_exclude_none=True)
async def login_user_test(
                     session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     response: Response,
                     ):
    user = await crud.get_user_by_email(email=form_data.username, session=session)

    if not user or not validate_password(password=form_data.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    SetTokenCookie(token=refresh_token).create_response(response=response)

    return {
        "access_token": access_token,
        }

@router.post('/logout')
async def logout(
                 token: Annotated[str, Depends(oauth2_scheme)],
                 response: Response,
                 ):
    
    response.delete_cookie(key='refresh_token')
    return {'message': 'Logout success'}