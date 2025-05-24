from pydantic import BaseModel, ConfigDict
from typing import Optional

class PostBase(BaseModel):
    name: str
    img: str
    description: str

class PostRead(PostBase):
    pass

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostUpdatePartial(PostCreate):

    name: Optional[str] = None
    img: Optional[str] = None
    description: Optional[str] = None

class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int