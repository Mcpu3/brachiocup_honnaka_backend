from pydantic import BaseModel


class ItemThumbnail(BaseModel):
    uuid: str
    base64: str

    class Config:
        from_attributes = True


class NewItemThumbnail(BaseModel):
    base64: str
