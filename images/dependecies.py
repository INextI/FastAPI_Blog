from fastapi import Depends, Path, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, Image
from . import crud

async def get_img_by_id(img_id: Annotated[int, Path],
                        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                        ) -> Image:
    img = await crud.get_image(img_id=img_id, session=session)
    if img is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No found img with this ID")
    return img