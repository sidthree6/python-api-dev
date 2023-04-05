from pydantic import BaseModel, EmailStr
from datetime import datetime


class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(BasePost):
    pass


class PostResponse(BasePost):
    pid: int
    published: bool
    created_at: datetime

    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    email: EmailStr
    password: str


class CreateUser(BaseUser):
    pass
