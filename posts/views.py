from fastapi import APIRouter, status, Depends, Request, UploadFile
from fastapi.responses import HTMLResponse
from .schemas import PostCreate, PostRead, Post, PostUpdate, PostUpdatePartial
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from . import crud
from .dependencies import post_by_id
from fastapi.templating import Jinja2Templates
from core.config import UPLOAD_DIR
import os

router = APIRouter(prefix='/posts', tags=['Posts'])
templates = Jinja2Templates(directory='templates')

@router.get('/', response_class= HTMLResponse)
async def get_posts_html(request: Request,
                         session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
                         ):
    posts: List[PostRead] = await crud.get_posts(session=session)
    return templates.TemplateResponse('home.html', {
        'request': request,
        'posts': posts,
    })

@router.get('/', response_model=List[Post])
async def get_posts(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]) -> Post:
    return await crud.get_posts(session=session)

@router.post('/')
async def create_post(post: PostCreate,
                      session: Annotated[AsyncSession, Depends(db_helper.session_getter)]) -> Post:
    
    return await crud.create_post(session=session, post_in=post)

@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int,
                        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]) -> None:
    await crud.delete_post(post_id=post_id, session=session)

@router.get('/{post_id}', response_model= Post)
async def get_post_by_id(post: Post = Depends(post_by_id)) -> Post:
    return post

@router.put('/{post_id}', response_model=Post)
async def update_post(
                      post_update: PostUpdate, 
                      session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                      post: Post = Depends(post_by_id)
                      ):
    return await crud.update_post(post_update=post_update, session=session, post=post)

@router.patch('/{post_id}', response_model=Post)
async def update_post_partial(post_update: PostUpdatePartial,
                              session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                              post: Post = Depends(post_by_id),
                              ):
    return await crud.update_post_partial(post_update=post_update, session=session, post=post)



@router.post('/image-upload')
async def upload_img(img_upload: UploadFile):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    import uuid

    ext = img_upload.filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        content = await img_upload.read()
        f.write(content)
    return {"filename": filename}

@router.get('image-viewer')
async def get_imgs():
    pass