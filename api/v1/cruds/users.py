from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.v1 import models, schemas


def read_user(database: Session, user_uuid: Optional[str]=None, username: Optional[str]=None) -> Optional[models.User]:
    user = None
    if user_uuid:
        user = read_user_by_uuid(database, user_uuid)
    if username:
        user = read_user_by_name(database, username)

    return user

def read_user_by_uuid(database: Session, user_uuid: str) -> Optional[models.User]:
    return database.query(models.User).filter(models.User.uuid ==user_uuid).first()

def read_user_by_name(database: Session, username: str) -> Optional[models.User]:
    return database.query(models.User).filter(models.User.username ==username).first()

def create_user(database: Session, signup: schemas.users.Signup) -> Optional[models.User]:
    hashed_password = CryptContext(["bcrypt"]).hash(signup.password)
    user = models.User(
        username = signup.username,
        hashed_password = hashed_password,
        display_name = signup.display_name
    )

    database.add(user)
    database.commit()
    database.refresh(user)

    return user
