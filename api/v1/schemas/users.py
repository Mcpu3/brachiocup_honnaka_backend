from pydantic import BaseModel

class Signup(BaseModel):
    username: str
    password: str
    display_name: str

class Signin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str

class User(BaseModel):
    user_uuid: str
    username: str
    display_name: str