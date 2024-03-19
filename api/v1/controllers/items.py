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

@api_router.get("/recommended", response_model=List[schemas.items.Item])
def get_recommended_items(group_uuid: str, size: int=10, current_user: models.User=Depends(get_current_user), database: Session=Depends(get_database)) -> List[schemas.items.Item]:
    group = authorize_group(database, group_uuid, current_user)

    item_purchasing_histories = cruds.item_purchasing_histories.read_item_purchasing_histories(database, current_user.uuid, group.uuid)
    if not item_purchasing_histories:
        raise HTTPException(status.HTTP_204_NO_CONTENT)

    quantities_grouped_by_item = {}
    for item_purchasing_history in item_purchasing_histories:
        if item_purchasing_history.item_expiration_date.item.uuid not in quantities_grouped_by_item:
            quantities_grouped_by_item[item_purchasing_history.item_expiration_date.item.uuid] = item_purchasing_history.quantity
        else:
            quantities_grouped_by_item[item_purchasing_history.item_expiration_date.item.uuid] += item_purchasing_history.quantity

    sorted_quantities_grouped_by_item = sorted(quantities_grouped_by_item.items(), key=lambda quantity_grouped_by_item: quantity_grouped_by_item[1], reverse=True)

    recommended_items = []
    for item_uuid, _ in sorted_quantities_grouped_by_item:
        recommended_item = cruds.items.read_item(database, item_uuid)
        if not recommended_item:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
        recommended_items.append(recommended_item)

    recommended_items = recommended_items[:size]

    return recommended_items

@api_router.get("/{item_uuid_or_barcode}", response_model=schemas.items.Item)
def get_item(group_uuid: str, item_uuid_or_barcode: str, current_user: models.User=Depends(get_current_user), database: Session=Depends(get_database)):
    group = authorize_group(database, group_uuid, current_user)

    item = cruds.items.read_item(database, item_uuid_or_barcode)
    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return item

@api_router.post("/")
def post_item(group_uuid: str, request: schemas.items.NewItem, _request: Request, current_user: models.User=Depends(get_current_user), database: Session=Depends(get_database)):
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

@api_router.delete("/{item_uuid}")
def delete_item(group_uuid: str, item_uuid: str, current_user: models.User=Depends(get_current_user), database: Session=Depends(get_database)):
    group = authorize_group(database, group_uuid, current_user)

    item = cruds.items.read_item(database, item_uuid)
    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    cruds.items.delete_item(database, item_uuid)

    return status.HTTP_200_OK
