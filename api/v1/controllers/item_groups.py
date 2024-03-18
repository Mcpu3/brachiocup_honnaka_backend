from typing import List
import urllib.parse

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.v1 import cruds, models, schemas
from api.v1.dependencies import get_database, get_current_user, authorize_group


api_router = APIRouter(prefix="/me/groups/{group_uuid}/item_groups", tags=["ItemGroups"])

@api_router.get("/", response_model=List[schemas.item_groups.ItemGroup])
def get_item_groups(group_uuid: str, current_user: models.User=Depends(get_current_user), database: Session=Depends(get_database)) -> List[schemas.item_groups.ItemGroup]:
    group = authorize_group(database, group_uuid, current_user)

    item_groups = cruds.item_groups.read_item_groups(database, group.uuid)
    if not item_groups:
        raise HTTPException(status.HTTP_204_NO_CONTENT)

    return item_groups

@api_router.get("/{item_group_uuid}", response_model=schemas.item_groups.ItemGroup)
def get_item_group(group_uuid: str, item_group_uuid: str, current_user: models.User=Depends(get_current_user),  database: Session=Depends(get_database)) -> schemas.item_groups.ItemGroup:
    group = authorize_group(database, group_uuid, current_user)

    item_group = cruds.item_groups.read_item_group(database, group.uuid, item_group_uuid)
    if not item_group:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return item_group

@api_router.post("/")
def post_item_group(group_uuid: str, request: schemas.item_groups.NewItemGroup, _request: Request, current_user: models.User=Depends(get_current_user), database: Session=Depends(get_database)):
    group = authorize_group(database, group_uuid, current_user, True)

    item_group = cruds.item_groups.create_item_group(database, group.uuid, request)
    if not item_group:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    response = {
        "Location": urllib.parse.urljoin(_request.url._url, f"./{item_group.uuid}")
    }

    return JSONResponse(response, status.HTTP_201_CREATED)
