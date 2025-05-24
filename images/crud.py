from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Image
from sqlalchemy import select
from fastapi import HTTPException, status, Path
from sqlalchemy.engine import Result
from typing import Annotated

async def create_img(filename: str, session: AsyncSession):

    img = Image(file_name = filename)
    session.add(img)
    await session.commit()
    await session.refresh(img)
    return img

async def get_images(session: AsyncSession)-> list[Image]:
    stmt = select(Image).order_by(Image.id)
    res: Result = await session.execute(stmt)
    if res is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="no imgs")
    imgs = res.scalars().all()
    return imgs

async def get_image(img_id: int, session: AsyncSession) -> Image:
    return await session.get(Image, img_id)