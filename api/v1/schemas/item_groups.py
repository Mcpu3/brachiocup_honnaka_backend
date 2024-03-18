from datetime import datetime
from pydantic import BaseModel
from typing import List

from api.v1.schemas import items_without_item_group


class ItemGroup(BaseModel):
    uuid: str
    name: str
    color: str
    items: List[items_without_item_group.ItemWithoutItemGroup]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NewItemGroup(BaseModel):
    name: str
    color: str
