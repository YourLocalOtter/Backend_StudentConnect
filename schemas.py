from typing import List, Union

from pydantic import BaseModel

class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    email: str
    fullname: str
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True