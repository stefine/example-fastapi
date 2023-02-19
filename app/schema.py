from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostRequest(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    created_at: datetime

    class Config:
        orm_mode = True


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True


class PostWithCounts(BaseModel):
    post: Post
    vote_count: int

    class Config:
        orm_mode = True


class UserRequest(BaseModel):
    email: EmailStr
    password: str


class UserProfile(BaseModel):
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: int
