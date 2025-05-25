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

templates = Jinja2Templates(directory='templates')

router = APIRouter(prefix='/new-posts', tags=['NewPosts'])

@router.post('/', response_model= NewPostBase)
async def create_post(
                      title: Annotated[str, Form()],
                      image_upload: Annotated[UploadFile, File()],
                      text: Annotated[str, Form()],
                      session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
                      ):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = image_upload.filename.split('.')[-1]
    filename = f"{uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as f:
        content = await image_upload.read()
        f.write(content)

    image = await img_crud.create_img(filename=filename, session=session)

    return await crud.create_post(title=title, img_id= image.id, text=text, session=session)

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


