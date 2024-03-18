from pydantic import BaseModel

from api.v1 import schemas


class ItemPurchasingHistory(BaseModel):
    uuid: str
    item_expiration_date: schemas.item_expiration_dates.ItemExpirationDate
    quantity: int

    class Config:
        from_attributes = True
