from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from api.v1 import models


def read_balances(database: Session, user_uuid: Optional[str]=None, group_uuid: Optional[str]=None) -> List[models.Balance]:
    balances = []
    if user_uuid:
        balances = read_balances_by_user(database, user_uuid)
    if group_uuid:
        balances = read_balances_by_group(database, group_uuid)

    return balances

def read_balances_by_user(database: Session, user_uuid: str) -> List[models.Balance]:
    return database.query(models.Balance).filter(models.Balance.user_uuid == user_uuid).all()

def read_balances_by_group(database: Session, group_uuid: str) -> List[models.Balance]:
    return database.query(models.Balance).filter(models.Balance.group_uuid == group_uuid).all()

def read_balance(database: Session, user_uuid: str, group_uuid: str) -> Optional[models.Balance]:
    return database.query(models.Balance).filter(and_(models.Balance.user_uuid == user_uuid, models.Balance.group_uuid == group_uuid)).first()

def create_balance(database: Session, user_uuid: str, group_uuid: str, new_balance: int) -> Optional[models.Balance]:
    balance = models.Balance(
        user_uuid=user_uuid,
        group_uuid=group_uuid,
        balance=new_balance
    )

    database.add(balance)
    database.commit()
    database.refresh(balance)

    return balance

def update_balance(database: Session, user_uuid: str, group_uuid: str, new_balance: int) -> Optional[models.Balance]:
    balance = read_balance(database, user_uuid, group_uuid)
    if balance:
        balance.balance = new_balance
        database.commit()
        database.refresh(balance)

    return balance
