from datetime import datetime
from pydantic import BaseModel
from typing import List

from api.v1.schemas import item_groups_without_items, item_expiration_dates, item_thumbnails


class Item(BaseModel):
    uuid: str
    item_group: item_groups_without_items.ItemGroupWithoutItems
    name: str
    barcode: str
    cost_price: int
    selling_price: int
    item_expiration_dates: List[item_expiration_dates.ItemExpirationDate]
    item_thumbnail: item_thumbnails.ItemThumbnail
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NewItem(BaseModel):
    item_group_uuid: str
    name: str
    barcode: str
    cost_price: int
    selling_price: int
    new_item_expiration_dates: List[item_expiration_dates.NewItemExpirationDate]
    new_item_thumbnail: item_thumbnails.NewItemThumbnail
