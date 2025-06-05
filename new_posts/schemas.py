from pydantic import BaseModel, ConfigDict
from images.schemas import Image

class NewPostBase(BaseModel):
    title: str
    img_id: int
    text: str
    author_id: int

class NewPostCreate(NewPostBase):
    pass

class NewPostRead(NewPostBase):
    title: str
    text:str

class NewPost(NewPostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class NewPostReadReact(NewPostRead):
    image: Image