from pydantic import BaseModel


class ItemGroupWithoutItems(BaseModel):
    uuid: str
    name: str
    color: str

    class Config:
        from_attributes = True
