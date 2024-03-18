from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from api.v1 import models, schemas


def read_item_purchasing_histories(database: Session, member: models.User, group_uuid: str):
    return database.query(models.ItemPurchasingHistory).filter(and_(models.ItemPurchasingHistory.user_uuid == member.uuid, models.ItemPurchasingHistory.group_uuid == group_uuid)).all()