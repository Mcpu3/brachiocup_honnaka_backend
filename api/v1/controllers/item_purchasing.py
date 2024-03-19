from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.v1 import cruds, models, schemas
from api.v1.dependencies import get_database, get_current_user, authorize_group


api_router = APIRouter(prefix="/me/groups/{group_uuid}/items/purchase", tags=["ItemPurchasing"])

@api_router.post("/")
def post_item_purchasing(group_uuid: str, request: schemas.item_purchasing.ItemPurchasing, current_user: models.User=Depends(get_current_user), database: Session=Depends(get_database)):
    group = authorize_group(database, group_uuid, current_user)

    item_expiration_date = cruds.item_expiration_dates.read_item_expiration_date(database, request.item_expiration_date_uuid)
    if not item_expiration_date:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    if item_expiration_date.quantity - request.quantity < 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    item_expiration_date = cruds.item_expiration_dates.update_quantity(database, item_expiration_date.uuid, item_expiration_date.quantity - request.quantity)
    if not item_expiration_date:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    balance = cruds.balances.read_balance(database, current_user.uuid, group.uuid)
    if not balance:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    if balance.balance - item_expiration_date.item.selling_price * request.quantity < 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    balance = cruds.balances.update_balance(database, current_user.uuid, group.uuid, balance.balance - item_expiration_date.item.selling_price * request.quantity)
    if not balance:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    item_purchasing_history = cruds.item_purchasing_histories.create_item_purchasing_history(database, current_user.uuid, group.uuid, request)
    if not item_purchasing_history:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    return status.HTTP_201_CREATED
