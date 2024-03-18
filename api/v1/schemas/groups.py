from pydantic import BaseModel


class Group(BaseModel):
    uuid: str
    groupname: str
    hashed_password: str
    display_name: str
    is_administrator: bool
    balance: int

    class Config:
        from_attributes = True


class Signup(BaseModel):
    groupname: str
    password: str
    display_name: str


class Signin(BaseModel):
    groupname: str
    password: str
