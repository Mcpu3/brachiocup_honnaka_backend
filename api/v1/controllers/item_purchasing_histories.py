from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from api.v1 import cruds, models, schemas
from api.v1.dependencies import get_database, get_current_user, authorize_group


api_router = APIRouter(prefix="/me/groups/{group_uuid}/item_purchasing_histories", tags=["ItemPurchasingHistories"])

@api_router.get("/", response_model=List[schemas.item_purchasing_histories.ItemPurchasingHistory])
def get_item_purchasing_histories(group_uuid: str, member: models.User=Depends(get_current_user),database: Session=Depends(get_database)) -> List[schemas.item_purchasing_histories.ItemPurchasingHistory]:
    _ = authorize_group(database, member, group_uuid)
    item_purchasing_history = cruds.item_purchasing_histories.read_item_purchasing_histories(database, member, group_uuid)
    if not item_purchasing_history:
        raise HTTPException(status.HTTP_204_NO_CONTENT)
    
    return item_purchasing_history