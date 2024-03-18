from typing import List
import urllib.parse

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.v1 import cruds, models, schemas
from api.v1.dependencies import get_database, get_current_user


api_router = APIRouter(prefix="/me/groups", tags=["Groups"])

@api_router.get("/", response_model=List[schemas.groups.Group])
def get_groups(current_user: models.User=Depends(get_current_user), database: Session=Depends(get_database)) -> List[schemas.groups.Group]:
    groups = cruds.groups.read_groups(database, current_user.uuid)
    if not groups:
        raise HTTPException(status.HTTP_204_NO_CONTENT)

    for group in groups:
        group.is_administrator = (current_user in group.administrators)

        balance = cruds.balances.read_balance(database, current_user.uuid, group.uuid)
        if not balance:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
        group.balance = balance.balance

    return groups

@api_router.get("/{group_uuid}", response_model=schemas.groups.Group)
def get_group(group_uuid: str, current_user: models.User=Depends(get_current_user), database: Session=Depends(get_database)) -> schemas.groups.Group:
    group = cruds.groups.read_group(database, group_uuid=group_uuid)
    if not group:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if current_user not in group.members:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    group.is_administrator = (current_user in group.administrators)

    balance = cruds.balances.read_balance(database, current_user.uuid, group.uuid)
    if not balance:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    group.balance = balance.balance

    return group

@api_router.post("/signup")
def signup(request: schemas.groups.Signup, _request: Request, current_user: models.User=Depends(get_current_user), database: Session=Depends(get_database)):
    group = cruds.groups.read_group(database, groupname=request.groupname)
    if group:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    group = cruds.groups.create_group(database, request)
    if not group:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    group = cruds.groups.update_group_members(database, group.uuid, [current_user])
    if not group:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    group = cruds.groups.update_group_administrators(database, group.uuid, [current_user])
    if not group:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    balance = cruds.balances.create_balance(database, current_user.uuid, group.uuid, 0)
    if not balance:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    response = {
        "Location": urllib.parse.urljoin(_request.url._url, f"./{group.uuid}")
    }

    return JSONResponse(response, status.HTTP_201_CREATED)

@api_router.post("/signin")
def signin(request: schemas.groups.Signin, _request: Request, current_user: models.User=Depends(get_current_user), database: Session=Depends(get_database)):
    group = cruds.groups.read_group(database, groupname=request.groupname)
    if not group:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if not CryptContext(["bcrypt"]).verify(request.password, group.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    group = cruds.groups.update_group_members(database, group.uuid, group.members + [current_user])
    if not group:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    balance = cruds.balances.create_balance(database, current_user.uuid, group.uuid, 0)
    if not balance:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    response = {
        "Location": urllib.parse.urljoin(_request.url._url, f"./{group.uuid}")
    }

    return JSONResponse(response, status.HTTP_201_CREATED)
