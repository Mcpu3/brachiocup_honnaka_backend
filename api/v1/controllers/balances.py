from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.v1 import cruds, models, schemas
from api.v1.dependencies import get_database, get_current_user, authorize_group


api_router = APIRouter(prefix="/me/groups/{group_uuid}", tags=["Balances"])

@api_router.post("/top_up_balance")
def top_up_balance(group_uuid: str, request: schemas.balances.TopUpBalance, current_user: models.User=Depends(get_current_user), database: Session=Depends(get_database)):
    group = authorize_group(database, group_uuid, current_user)

    balance = cruds.balances.read_balance(database, current_user.uuid, group.uuid)
    if not balance:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    balance = cruds.balances.update_balance(database, current_user.uuid, group.uuid, balance.balance + request.topped_up_balance)
    if not balance:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    return status.HTTP_201_CREATED
