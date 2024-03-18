from datetime import datetime
from pydantic import BaseModel

from api.v1.schemas import items_without_item_expiration_dates


class ItemExpirationDate(BaseModel):
    uuid: str
    item: items_without_item_expiration_dates.ItemWithoutItemExpirationDates
    expiration_date: datetime
    quantity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NewItemExpirationDate(BaseModel):
    expiration_date: datetime
    quantity: int
