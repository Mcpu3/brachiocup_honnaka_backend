from pydantic import BaseModel


class Token(BaseModel):
    access_token: str


class User(BaseModel):
    user_uuid: str
    username: str
    display_name: str

    class Config:
        from_attributes = True


class Signup(BaseModel):
    username: str
    password: str
    display_name: str
