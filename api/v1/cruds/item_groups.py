from typing import List, Optional

from passlib.context import CryptContext
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session


from api.v1 import models, schemas

def read_item_groups(database: Session,  group_uuid: str) -> List[models.ItemGroup]:
    return database.query(models.ItemGroup).filter(models.ItemGroup.group_uuid == group_uuid).all()

def read_item_group(database: Session, group_uuid: str, item_group_uuid: str) -> Optional[models.ItemGroup]:
    return database.query(models.ItemGroup).filter(and_(models.ItemGroup.group_uuid == group_uuid, models.ItemGroup.uuid == item_group_uuid)).first()

def create_item_group(database: Session, group_uuid: str, new_item_group: schemas.item_groups.NewItemGroup) -> Optional[models.ItemGroup]:
    item_group = models.ItemGroup(
        group_uuid=group_uuid,
        name=new_item_group.name,
        color=new_item_group.color
    )

    database.add(item_group)
    database.commit()
    database.refresh(item_group)

    return item_group
