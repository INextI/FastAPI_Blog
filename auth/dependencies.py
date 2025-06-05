from typing import Annotated
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends, status
from .views import oauth2_scheme
from core.config import settings
from core.models import db_helper
from .utils import decode_access_token
from users import crud
from core.models import User

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
                           ) -> User:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        user = await crud.get_user_by_id(user_id=user_id, session=session)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"error: {e}")


async def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)],
                             session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
                             ):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        user = await crud.get_user_by_id(user_id=user_id, session=session)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return int(user_id)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"error: {e}")