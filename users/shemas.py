from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    nickname: str


class UserCreate(UserBase):
    is_admin: bool = False
    email: EmailStr
    password: str

class UserBaseFull(UserBase):
    is_admin: bool
    email: EmailStr
    hashed_password: str
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str