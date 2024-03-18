from datetime import datetime
import os
import urllib.parse
import uuid

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_CONNECTION_STRING = urllib.parse.quote_plus("Driver={ODBC Driver 18 for SQL Server};Server=tcp:brachiocup-honnaka-backend.database.windows.net,1433;Database=brachiocup-honnaka-backend;Uid=brachiocup-honnaka-backend;Pwd={%s};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;" % DATABASE_PASSWORD)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc:///?odbc_connect={DATABASE_CONNECTION_STRING}"
database = SQLAlchemy(app)
migrate = Migrate(app, database)


class User(database.Model):
    __tablename__ ="Users"

    uuid = database.Column(database.String(48), primary_key=True, default=uuid.uuid4)
    username = database.Column(database.String(48), unique=True, nullable=False)
    hashed_password = database.Column(database.Unicode, nullable=False)
    display_name = database.Column(database.Unicode, nullable=False)
    created_at = database.Column(database.DateTime, nullable=False, default=datetime.now)
    updated_at = database.Column(database.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    groups = database.relationship("Group", secondary="GroupMembers", back_populates="members")
    administrated_groups = database.relationship("Group", secondary="GroupAdministrators", back_populates="administrators")
    balances = database.relationship("Balance", back_populates="user")
    item_purchasing_histories = database.relationship("ItemPurchasingHistory", back_populates="user")


class Group(database.Model):
    __tablename__ = "Groups"

    uuid = database.Column(database.String(48), primary_key=True, default=uuid.uuid4)
    groupname = database.Column(database.String(48), unique=True, nullable=False)
    hashed_password = database.Column(database.Unicode, nullable=False)
    display_name = database.Column(database.Unicode, nullable=False)
    created_at = database.Column(database.DateTime, nullable=False, default=datetime.now)
    updated_at = database.Column(database.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    members = database.relationship("User", secondary="GroupMembers", back_populates="groups")
    administrators = database.relationship("User", secondary="GroupAdministrators", back_populates="administrated_groups")
    balances = database.relationship("Balance", back_populates="group")
    item_groups = database.relationship("ItemGroup", back_populates="group")
    items = database.relationship("Item", back_populates="group")
    item_purchasing_histories = database.relationship("ItemPurchasingHistory", back_populates="group")


class GroupMember(database.Model):
    __tablename__ = "GroupMembers"

    user_uuid = database.Column(database.String(48), database.ForeignKey("Users.uuid"), primary_key=True)
    group_uuid = database.Column(database.String(48), database.ForeignKey("Groups.uuid"), primary_key=True)


class GroupAdministrator(database.Model):
    __tablename__ = "GroupAdministrators"

    user_uuid = database.Column(database.String(48), database.ForeignKey("Users.uuid"), primary_key=True)
    group_uuid = database.Column(database.String(48), database.ForeignKey("Groups.uuid"), primary_key=True)


class Balance(database.Model):
    __tablename__ = "Balances"

    uuid = database.Column(database.String(48), primary_key=True, default=uuid.uuid4)
    user_uuid = database.Column(database.String(48), database.ForeignKey("Users.uuid"), nullable=False)
    group_uuid = database.Column(database.String(48), database.ForeignKey("Groups.uuid"), nullable=False)
    balance = database.Column(database.Integer, nullable=False)
    created_at = database.Column(database.DateTime, nullable=False, default=datetime.now)
    updated_at = database.Column(database.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    user = database.relationship("User", back_populates="balances")
    group = database.relationship("Group", back_populates="balances")


class ItemGroup(database.Model):
    __tablename__ = "ItemGroups"

    uuid = database.Column(database.String(48), primary_key=True, default=uuid.uuid4)
    group_uuid = database.Column(database.String(48), database.ForeignKey("Groups.uuid"), nullable=False)
    name = database.Column(database.Unicode, nullable=False)
    color = database.Column(database.Unicode, nullable=False)
    created_at = database.Column(database.DateTime, nullable=False, default=datetime.now)
    updated_at = database.Column(database.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    group = database.relationship("Group", back_populates="item_groups")
    items = database.relationship("Item", back_populates="item_group")


class Item(database.Model):
    __tablename__ = "Items"

    uuid = database.Column(database.String(48), primary_key=True, default=uuid.uuid4)
    group_uuid = database.Column(database.String(48), database.ForeignKey("Groups.uuid"), nullable=False)
    item_group_uuid = database.Column(database.String(48), database.ForeignKey("ItemGroups.uuid"), nullable=False)
    name = database.Column(database.Unicode, nullable=False)
    barcode = database.Column(database.Unicode, nullable=False)
    cost_price = database.Column(database.Integer, nullable=False)
    selling_price = database.Column(database.Integer, nullable=False)
    created_at = database.Column(database.DateTime, nullable=False, default=datetime.now)
    updated_at = database.Column(database.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    group = database.relationship("Group", back_populates="items")
    item_group = database.relationship("ItemGroup", back_populates="items")
    item_expiration_dates = database.relationship("ItemExpirationDate", back_populates="item")
    item_thumbnail = database.relationship("ItemThumbnail", back_populates="item", uselist=False)


class ItemExpirationDate(database.Model):
    __tablename__ = "ItemExpirationDates"

    uuid = database.Column(database.String(48), primary_key=True, default=uuid.uuid4)
    item_uuid = database.Column(database.String(48), database.ForeignKey("Items.uuid"), nullable=False)
    expiration_date = database.Column(database.DateTime, nullable=False)
    quantity = database.Column(database.Integer, nullable=False)
    created_at = database.Column(database.DateTime, nullable=False, default=datetime.now)
    updated_at = database.Column(database.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    item = database.relationship("Item", back_populates="item_expiration_dates")
    item_purchasing_histories = database.relationship("ItemPurchasingHistory", back_populates="item_expiration_date")


class ItemThumbnail(database.Model):
    __tablename__ = "ItemThumbnails"

    uuid = database.Column(database.String(48), primary_key=True, default=uuid.uuid4)
    item_uuid = database.Column(database.String(48), database.ForeignKey("Items.uuid"), nullable=False)
    base64 = database.Column(database.Unicode, nullable=False)
    created_at = database.Column(database.DateTime, nullable=False, default=datetime.now)
    updated_at = database.Column(database.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    item = database.relationship("Item", back_populates="item_thumbnail")


class ItemPurchasingHistory(database.Model):
    __tablename__ = "ItemPurchasingHistories"

    uuid = database.Column(database.String(48), primary_key=True, default=uuid.uuid4)
    user_uuid = database.Column(database.String(48), database.ForeignKey("Users.uuid"), nullable=False)
    group_uuid = database.Column(database.String(48), database.ForeignKey("Groups.uuid"), nullable=False)
    item_expiration_date_uuid = database.Column(database.String(48), database.ForeignKey("ItemExpirationDates.uuid"), nullable=False)
    created_at = database.Column(database.DateTime, nullable=False, default=datetime.now)
    updated_at = database.Column(database.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    user = database.relationship("User", back_populates="item_purchasing_histories")
    group = database.relationship("Group", back_populates="item_purchasing_histories")
    item_expiration_date = database.relationship("ItemExpirationDate", back_populates="item_purchasing_histories")
