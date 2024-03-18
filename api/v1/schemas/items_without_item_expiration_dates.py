from datetime import datetime
from pydantic import BaseModel

from api.v1.schemas import item_groups_without_items, item_thumbnails


class ItemWithoutItemExpirationDates(BaseModel):
    uuid: str
    item_group: item_groups_without_items.ItemGroupWithoutItems
    name: str
    barcode: str
    cost_price: int
    selling_price: int
    item_thumbnail: item_thumbnails.ItemThumbnail
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
