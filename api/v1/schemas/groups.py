from datetime import datetime
from pydantic import BaseModel


class Group(BaseModel):
    uuid: str
    groupname: str
    display_name: str
    is_administrator: bool
    balance: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Signup(BaseModel):
    groupname: str
    password: str
    display_name: str


class Signin(BaseModel):
    groupname: str
    password: str
