from pydantic import BaseModel


class NewGroup(BaseModel):
    groupname: str
    password: str
    display_name: str

class Group(BaseModel):
    groupname: str
    hashed_password: str
    display_name: str