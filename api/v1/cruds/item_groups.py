from typing import List, Optional

from passlib.context import CryptContext
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session


from api.v1 import models, schemas

def read_item_groups(database: Session,  group_uuid: str) -> Optional[models.ItemGroup]:
    return database.query(models.ItemGroup).filter(models.ItemGroup.group_uuid == group_uuid).all()