from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from api.v1 import models, schemas


def read_item_thumbnails(database: Session, item_uuid: str) -> List[models.ItemThumbnail]:
    return database.query(models.ItemThumbnail).filter(models.ItemThumbnail.item_uuid == item_uuid).all()

def read_item_thumbnail(database: Session, item_uuid: str, item_thumbnail_uuid: str) -> Optional[models.ItemThumbnail]:
    return database.query(models.ItemThumbnail).filter(and_(models.ItemThumbnail.item_uuid == item_uuid, models.ItemTHumbnail.uuid == item_thumbnail_uuid)).first()

def create_item_thumbnail(database: Session, item_uuid: str, new_item_thumbnail: schemas.item_thumbnails.new_item_thumbnails) -> Optional[models.ItemThumbnail]:
    item_thumbnail = models.ItemThumbnail(
        item_uuid=item_uuid,
        base64=new_item_thumbnail.base64
    )

    database.add(item_thumbnail)
    database.commit()
    database.refresh(item_thumbnail)

    return item_thumbnail
