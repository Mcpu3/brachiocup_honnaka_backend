from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from api.v1 import models, schemas


def read_items(database: Session, group_uuid: str) -> List[models.Item]:
    return database.query(models.Item).filter(models.Item.group_uuid == group_uuid).all()

def read_item(database: Session, item_uuid_or_barcode: str) -> Optional[models.Item]:
    return database.query(models.Item).filter(or_(models.Item.uuid == item_uuid_or_barcode, models.Item.barcode == item_uuid_or_barcode)).first()

def create_item(database: Session, group_uuid: str, new_item: schemas.items.NewItem) -> Optional[models.Item]:
    item = models.Item(
        group_uuid=group_uuid,
        item_group_uuid=new_item.item_group_uuid,
        name=new_item.name,
        barcode=new_item.barcode,
        cost_price=new_item.cost_price,
        selling_price=new_item.selling_price
    )

    database.add(item)
    database.commit()
    database.refresh(item)

    return item
