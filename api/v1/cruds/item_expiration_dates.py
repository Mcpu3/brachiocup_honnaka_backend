from typing import List, Optional

from sqlalchemy.orm import Session

from api.v1 import models, schemas


def read_item_expiration_dates(database: Session, item_uuid: str) -> List[models.ItemExpirationDate]:
    return database.query(models.ItemExpirationDate).filter(models.ItemExpirationDate.item_uuid == item_uuid).all()

def read_item_expiration_date(database: Session, item_expiration_date_uuid: str) -> Optional[models.ItemExpirationDate]:
    return database.query(models.ItemExpirationDate).filter(models.ItemExpirationDate.uuid == item_expiration_date_uuid).first()

def create_item_expiration_date(database: Session, item_uuid: str, new_item_expiration_date: schemas.item_expiration_dates.NewItemExpirationDate) -> Optional[models.ItemExpirationDate]:
    item_expiration_date = models.ItemExpirationDate(
        item_uuid=item_uuid,
        expiration_date=new_item_expiration_date.expiration_date,
        quantity=new_item_expiration_date.quantity
    )

    database.add(item_expiration_date)
    database.commit()
    database.refresh(item_expiration_date)

    return item_expiration_date

def update_quantity(database: Session, item_expiration_date_uuid: str, new_quantity: int) -> Optional[models.ItemExpirationDate]:
    item_expiration_date = read_item_expiration_date(database, item_expiration_date_uuid)
    if item_expiration_date:
        item_expiration_date.quantity = new_quantity
        database.commit()
        database.refresh(item_expiration_date)

    return item_expiration_date
