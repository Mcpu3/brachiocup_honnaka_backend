from pydantic import BaseModel

class Helloworld(BaseModel):
    name: str

    class Config:
        orm_mode = True