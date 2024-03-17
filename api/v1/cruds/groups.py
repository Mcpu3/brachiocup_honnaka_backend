from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.v1 import models, schemas


def read_group(database: Session, group_uuid: str) -> Optional[models.Group]:
    return database.query(models.Group).filter(models.Group.group_uuid == group_uuid).first()

def create_group(database: Session, user: models.User, new_group: schemas.groups.NewGroup) -> Optional[models.Group]:
    hashed_password = CryptContext(["bcrypt"]).hash(new_group.password)
    group = models.Group(
        groupname = new_group.groupname,
        hashed_password = hashed_password, 
        display_name = new_group.display_name
    )

    database.add(group)
    database.commit()
    database.refresh(group)

    group.members.append(user)
    group.administrators.append(user)
    database.commit()
    database.refresh(group)

    return group
