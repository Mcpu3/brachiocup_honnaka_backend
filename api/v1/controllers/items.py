from typing import List
import urllib.parse

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.v1 import cruds, models, schemas
from api.v1.dependencies import get_database, get_current_user, authorize_group


api_router = APIRouter(prefix="/me/groups/{group_uuid}/items", tags=["Items"])

@api_router.get("/", response_model=List[schemas.items.Item])
def get_items(group_uuid: str, current_user: models.User=Depends(get_current_user), database: Session=Depends(get_database)) -> List[schemas.items.Item]:
    group = authorize_group(database, group_uuid, current_user)

    items = cruds.items.read_items(database, group.uuid)
    if not items:
        raise HTTPException(status.HTTP_204_NO_CONTENT)

    return items

@api_router.get("/{item_uuid}", response_model=schemas.items.Item)
def get_item(group_uuid: str, item_uuid: str, current_user: models.User=Depends(get_current_user), database: Session=Depends(get_database)):
    group = authorize_group(database, group_uuid, current_user)

    item = cruds.items.read_item(database, item_uuid)
    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return item

@api_router.post("/")
def post_item_group(group_uuid: str, request: schemas.items.NewItem, _request: Request, current_user: models.User=Depends(get_current_user), database: Session=Depends(get_database)):
    group = authorize_group(database, group_uuid, current_user, True)

    item = cruds.items.create_item(database, group.uuid, request)
    if not item:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    for new_item_expiration_date in request.new_item_expiration_dates:
        item_expiration_date = cruds.item_expiration_dates.create_item_expiration_date(database, item.uuid, new_item_expiration_date)
        if not item_expiration_date:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)

    item_thumbnail = cruds.item_thumbnails.create_item_thumbnail(database, item.uuid, request.new_item_thumbnail)
    if not item_thumbnail:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    response = {
        "Location": urllib.parse.urljoin(_request.url._url, f"./{item.uuid}")
    }

    return JSONResponse(response, status.HTTP_201_CREATED)
