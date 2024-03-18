from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from api.v1 import models, schemas


def read_item_purchasing_histories(database: Session, user_uuid: str, group_uuid: str) -> List[models.ItemPurchasingHistory]:
    return database.query(models.ItemPurchasingHistory).filter(and_(models.ItemPurchasingHistory.user_uuid == user_uuid, models.ItemPurchasingHistory.group_uuid == group_uuid)).all()

def create_item_purchasing_history(database: Session, user_uuid: str, group_uuid: str, request: schemas.item_purchasing.ItemPurchasing) -> Optional[models.ItemPurchasingHistory]:
    item_purchasing_history = models.ItemPurchasingHistory(
        user_uuid=user_uuid,
        group_uuid=group_uuid,
        item_expiration_date_uuid=request.item_expiration_date_uuid,
        quantity=request.quantity
    )

    database.add(item_purchasing_history)
    database.commit()
    database.refresh(item_purchasing_history)

    return item_purchasing_history
