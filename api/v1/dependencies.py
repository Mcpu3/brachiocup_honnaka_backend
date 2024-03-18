import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from api.v1 import cruds, models
from api.v1.database import LocalSession


def get_database():
    database = LocalSession()
    try:
        yield database
    finally:
        database.close()

def get_current_user(access_token: str=Depends(OAuth2PasswordBearer("/api/v1/signin")), database: Session=Depends(get_database)) -> models.User:
    try:
        data = jwt.decode(access_token, os.getenv("SECRET_KEY"), "HS256")
        username = data.get("sub")
        if not username:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    user = cruds.users.read_user(database, username=username)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return user

def authorize_group(database: Session, member: models.User, group_uuid: str, only_administrator: bool=False):
    group = cruds.groups.read_group(database, group_uuid)
    if not group:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if member not in group.members:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if only_administrator:
        if member not in group.administrators:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    
    return group