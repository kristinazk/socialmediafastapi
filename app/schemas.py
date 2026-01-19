from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# defining what a post should look like
class PostBase(BaseModel):  # inheriting from BaseModel makes it a special pydantic object
    title: str
    content: str
    published: bool = True  # defaults to true

class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponse

    class Config:
        from_attributes = True


class PostOutput(BaseModel):
    Post: PostResponse
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int]


class InputVote(BaseModel):
    post_id: int
    placing_vote: bool  # True for voting False for removing vote
