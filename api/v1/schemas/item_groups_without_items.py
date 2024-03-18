from datetime import datetime
from pydantic import BaseModel


class ItemGroupWithoutItems(BaseModel):
    uuid: str
    name: str
    color: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
