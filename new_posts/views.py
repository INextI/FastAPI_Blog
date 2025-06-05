from fastapi import (
    Depends, 
    APIRouter, 
    HTTPException, 
    status, 
    Form, 
    UploadFile, 
    File,
    Request,
    )
from fastapi.responses import HTMLResponse
from core.models import NewPost
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import NewPostBase, NewPostCreate, NewPostRead
from typing import Annotated
from core.models import db_helper
import os
from core.config import UPLOAD_DIR
from uuid import uuid4
from images import crud as img_crud
from . import crud
from fastapi.templating import Jinja2Templates
from auth.dependencies import get_current_user_id
from users.shemas import UserBaseFull

templates = Jinja2Templates(directory='templates')

router = APIRouter(prefix='/new-posts', tags=['NewPosts'])

@router.post('/', response_model= NewPostBase)
async def create_post(
                      title: Annotated[str, Form()],
                      image_upload: Annotated[UploadFile, File()],
                      text: Annotated[str, Form()],
                      session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                      user_id: int = Depends(get_current_user_id),
                      ):

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = image_upload.filename.split('.')[-1]
    filename = f"{uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    image = await img_crud.create_img(filename=filename, session=session)

    post = await crud.create_post(title=title, img_id= image.id, text=text, session=session, user_id=user_id)
    
    if (image and post) is not None:
        with open(file_path, "wb") as f:
            content = await image_upload.read()
            f.write(content)
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Не смогли создать пользователя или изображение")
    return post

@router.get('/', response_model=list[NewPostRead])
async def get_posts(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
    ):
    posts: list[NewPostRead] = await crud.get_posts(session=session)

    return posts

"""
@router.get('/', response_class=HTMLResponse)
async def get_posts(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
    ):
    posts: list[NewPostRead] = await crud.get_posts(session=session)

    return templates.TemplateResponse('home_img.html', {
        'request': request,
        'posts' : posts
    })
"""
    
@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int,
                      session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
                      ):
    await crud.delete_post(post_id=post_id, session=session)


