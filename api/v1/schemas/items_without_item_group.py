from pydantic import BaseModel
from typing import List

from api.v1.schemas import item_expiration_dates, item_thumbnails


class ItemWithoutItemGroup(BaseModel):
    uuid: str
    name: str
    barcode: str
    cost_price: int
    selling_price: int
    item_expiration_dates: List[item_expiration_dates.ItemExpirationDate]
    item_thumbnail: item_thumbnails.ItemThumbnail

    class Config:
        from_attributes = True
