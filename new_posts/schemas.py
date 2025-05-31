from pydantic import BaseModel, ConfigDict

class NewPostBase(BaseModel):
    title: str
    img_id: int
    text: str
    author: str

class NewPostCreate(NewPostBase):
    pass

class NewPostRead(NewPostBase):
    title: str
    text:str

class NewPost(NewPostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
