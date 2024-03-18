import urllib.parse

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.v1 import cruds, models, schemas
from api.v1.dependencies import get_database, get_current_user, authorize_group

api_router = APIRouter(prefix="/me/groups/{group_uuid}/items/purchase", tags=["ItemPurchasing"])

@api_router.post("/")
def post_item_purchase(group_uuid: str, request: schemas.item_purchasing.ItemPurchasing, _request: Request, current_user: models.User=Depends(get_current_user), database: Session=Depends(get_database)):
    _ = authorize_group(database, group_uuid, current_user)

    item_purchasing_history = cruds.item_purchasing_histories.create_item_purchasing_history(database, current_user, group_uuid, request)
    if not item_purchasing_history:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    response = {
        "Location": urllib.parse.urljoin(_request.url._url, f"./{item_purchasing_history.uuid}")
    }

    return JSONResponse(response, status.HTTP_201_CREATED)

