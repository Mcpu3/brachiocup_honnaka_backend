from datetime import datetime
from pydantic import BaseModel


class ItemThumbnail(BaseModel):
    uuid: str
    base64: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NewItemThumbnail(BaseModel):
    base64: str
