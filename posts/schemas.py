from pydantic_settings import BaseSettings

class PostBase(BaseSettings):
    name: str
    img: str
    description: str

class PostRead(PostBase):
    pass

class PostCreate(PostBase):
    pass