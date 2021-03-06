from typing import List, Union

from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    email: str
    realname: str
    username: str
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class UserPrivate(User):
    email: str
    realname: str
    username: str

class UserSemiPrivate(User):
    realname: str

class UserAuthenticateReq(BaseModel):
    email: str
    password: str

class ForumBase(BaseModel):
    name: str
    desc: str
    banner_url: str

class Forum(ForumBase):
    id: int

class TopicBase(BaseModel):
    name: str
    
class Topic(TopicBase):
    who_started_id: int
    id: int

class PostBase(BaseModel):
    content: str
    poster_id: int

class Post(PostBase):
    pass