from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Unicode
from sqlalchemy.orm import relationship

from api.v1.database import Base


class User(Base):
    __tablename__ ="Users"

    uuid = Column(String(48), primary_key=True, default=uuid.uuid4)
    username = Column(String(48), unique=True, nullable=False)
    hashed_password = Column(Unicode, nullable=False)
    display_name = Column(Unicode, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    groups = relationship("Group", secondary="GroupMembers", back_populates="members")
    administrated_groups = relationship("Group", secondary="GroupAdministrators", back_populates="administrators")
    balances = relationship("Balance", back_populates="user")
    item_purchasing_histories = relationship("ItemPurchasingHistory", back_populates="user")


class Group(Base):
    __tablename__ = "Groups"

    uuid = Column(String(48), primary_key=True, default=uuid.uuid4)
    groupname = Column(String(48), unique=True, nullable=False)
    hashed_password = Column(Unicode, nullable=False)
    display_name = Column(Unicode, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    members = relationship("User", secondary="GroupMembers", back_populates="groups")
    administrators = relationship("User", secondary="GroupAdministrators", back_populates="administrated_groups")
    balances = relationship("Balance", back_populates="group")
    item_groups = relationship("ItemGroup", back_populates="group")


class GroupMember(Base):
    __tablename__ = "GroupMembers"

    user_uuid = Column(String(48), ForeignKey("Users.uuid"), primary_key=True)
    group_uuid = Column(String(48), ForeignKey("Groups.uuid"), primary_key=True)


class GroupAdministrator(Base):
    __tablename__ = "GroupAdministrators"

    user_uuid = Column(String(48), ForeignKey("Users.uuid"), primary_key=True)
    group_uuid = Column(String(48), ForeignKey("Groups.uuid"), primary_key=True)


class Balance(Base):
    __tablename__ = "Balances"

    uuid = Column(String(48), primary_key=True, default=uuid.uuid4)
    user_uuid = Column(String(48), ForeignKey("Users.uuid"), nullable=False)
    group_uuid = Column(String(48), ForeignKey("Groups.uuid"), nullable=False)
    balance = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="balances")
    group = relationship("Group", back_populates="balances")


class ItemGroup(Base):
    __tablename__ = "ItemGroups"

    uuid = Column(String(48), primary_key=True, default=uuid.uuid4)
    group_uuid = Column(String(48), ForeignKey("Groups.uuid"), nullable=False)
    name = Column(Unicode, nullable=False)
    color = Column(Unicode, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    group = relationship("Group", back_populates="item_groups")
    items = relationship("Item", back_populates="item_group")


class Item(Base):
    __tablename__ = "Items"

    uuid = Column(String(48), primary_key=True, default=uuid.uuid4)
    item_group_uuid = Column(String(48), ForeignKey("ItemGroups.uuid"), nullable=False)
    name = Column(Unicode, nullable=False)
    barcode = Column(Unicode, nullable=False)
    cost_price = Column(Integer, nullable=False)
    selling_price = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    item_group = relationship("ItemGroup", back_populates="items")
    item_thumbnail = relationship("ItemThumbnail", back_populates="item")
    item_expiration_dates = relationship("ItemExpirationDate", back_populates="item")


class ItemExpirationDate(Base):
    __tablename__ = "ItemExpirationDates"

    uuid = Column(String(48), primary_key=True, default=uuid.uuid4)
    item_uuid = Column(String(48), ForeignKey("Items.uuid"), nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    item = relationship("Item", back_populates="item_expiration_dates")
    item_purchasing_histories = relationship("ItemPurchasingHistory", back_populates="item_expiration_date")


class ItemThumbnail(Base):
    __tablename__ = "ItemThumbnails"

    uuid = Column(String(48), primary_key=True, default=uuid.uuid4)
    item_uuid = Column(String(48), ForeignKey("Items.uuid"), nullable=False)
    base64 = Column(Unicode, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    item = relationship("Item", back_populates="item_thumbnail")


class ItemPurchasingHistory(Base):
    __tablename__ = "ItemPurchasingHistories"

    uuid = Column(String(48), primary_key=True, default=uuid.uuid4)
    user_uuid = Column(String(48), ForeignKey("Users.uuid"), nullable=False)
    item_expiration_date_uuid = Column(String(48), ForeignKey("ItemExpirationDates.uuid"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="item_purchasing_histories")
    item_expiration_date = relationship("ItemExpirationDate", back_populates="item_purchasing_histories")
