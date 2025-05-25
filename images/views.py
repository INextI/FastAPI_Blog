from fastapi import APIRouter, Depends, UploadFile, Path, HTTPException, status
from fastapi.responses import FileResponse
from .schemas import ImageBase
from core.models import db_helper
from core.models import Image
from core.config import UPLOAD_DIR
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
import os
import uuid
from . import crud
from .dependecies import get_img_by_id

router = APIRouter(prefix='/images', tags=['img'])

@router.post('/', response_model=ImageBase)
async def upload_img(img_upload: UploadFile,
                     session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
                     ):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    ext = img_upload.filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        content = await img_upload.read()
        f.write(content)
    return await crud.create_img(filename=filename, session=session)


@router.get('/', response_model=list[ImageBase])
async def get_images(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):

    return await crud.get_images(session=session)

@router.get('/{img_id}', response_class=FileResponse)
async def get_image(img: Image = Depends(get_img_by_id)):
    filename = img.file_name
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='Image not found')
    
    return FileResponse(path=file_path, media_type='image/jpeg') #filename=filename

@router.get('/{img_id}', response_model=ImageBase)
async def get_image_old(
                    img_id: Annotated[int, Path],
                    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
                    ):
    return await crud.get_image(img_id=img_id, session=session)