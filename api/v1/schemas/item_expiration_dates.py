from datetime import datetime
from pydantic import BaseModel


class ItemExpirationDate(BaseModel):
    uuid: str
    expiration_date: datetime
    quantity: int

    class Config:
        from_attributes = True


class NewItemExpirationDate(BaseModel):
    expiration_date: datetime
    quantity: int
