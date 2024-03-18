from typing import List, Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.v1 import models, schemas


def read_groups(database: Session, member_uuid: str) -> List[models.Group]:
    return database.query(models.Group).filter(models.Group.members.any(uuid=member_uuid)).all()

def read_group(database: Session, group_uuid: Optional[str]=None, groupname: Optional[str]=None) -> Optional[models.Group]:
    group = None
    if group_uuid:
        group = read_group_by_uuid(database, group_uuid)
    if groupname:
        group = read_group_by_name(database, groupname)

    return group

def read_group_by_uuid(database: Session, group_uuid: str) -> Optional[models.Group]:
    return database.query(models.Group).filter(models.Group.uuid == group_uuid).first()

def read_group_by_name(database: Session, groupname: str) -> Optional[models.Group]:
    return database.query(models.Group).filter(models.Group.groupname == groupname).first()

def create_group(database: Session, signup: schemas.groups.Signup) -> Optional[models.Group]:
    hashed_password = CryptContext(["bcrypt"]).hash(signup.password)
    group = models.Group(
        groupname=signup.groupname,
        hashed_password=hashed_password,
        display_name=signup.display_name
    )

    database.add(group)
    database.commit()
    database.refresh(group)

    return group

def update_group_members(database: Session, group_uuid: str, new_members: List[models.User]) -> Optional[models.Group]:
    group = read_group(database, group_uuid=group_uuid)
    if group:
        group.members = new_members
        database.commit()
        database.refresh(group)

    return group

def update_group_administrators(database: Session, group_uuid: str, new_administrators: List[models.User]) -> Optional[models.Group]:
    group = read_group(database, group_uuid=group_uuid)
    if group:
        group.administrators = new_administrators
        database.commit()
        database.refresh(group)

    return group
