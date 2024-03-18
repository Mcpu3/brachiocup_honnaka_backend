from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from api.v1 import cruds, models, schemas
from api.v1.dependencies import get_database, get_current_user, authorize_group


api_router = APIRouter(prefix="/me/groups/{group_uuid}/item_groups", tags=["ItemGroups"])

@api_router.get("/", response_model=List[schemas.item_groups.ItemGroup])
def get_item_groups(group_uuid: str, member: models.User=Depends(get_current_user), database: Session=Depends(get_database)) -> List[schemas.item_groups.ItemGroup]:
    authorize_group(database, member, group_uuid)
    item_groups = cruds.item_groups.read_item_groups(database, group_uuid)
    if not item_groups:
        raise HTTPException(status.HTTP_204_NO_CONTENT)
    
    return item_groups


    

