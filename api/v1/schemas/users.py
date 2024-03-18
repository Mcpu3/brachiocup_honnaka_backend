from datetime import datetime
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str


class User(BaseModel):
    uuid: str
    username: str
    display_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Signup(BaseModel):
    username: str
    password: str
    display_name: str
