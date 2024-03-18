from pydantic import BaseModel
from typing import List

from api.v1.schemas import items_without_item_group


class ItemGroup(BaseModel):
    uuid: str
    name: str
    color: str
    items: List[items_without_item_group.ItemWithoutItemGroup]

    class Config:
        from_attributes = True


class NewItemGroup(BaseModel):
    name: str
    color: str
