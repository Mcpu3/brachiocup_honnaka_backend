from pydantic import BaseModel


class HelloWorld(BaseModel):
    name: str

    class Config:
        from_attributes = True
