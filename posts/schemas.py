from pydantic import BaseModel, ConfigDict

class PostBase(BaseModel):
    name: str
    img: str
    description: str

class PostRead(PostBase):
    pass

class PostCreate(PostBase):
    pass

class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int