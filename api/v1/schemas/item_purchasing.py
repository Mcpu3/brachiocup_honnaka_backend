from pydantic import BaseModel


class ItemPurchasing(BaseModel):
    item_expiration_date_uuid: str
    quantity: int
