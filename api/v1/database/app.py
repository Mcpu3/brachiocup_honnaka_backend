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


class HelloWorld(database.Model):
    __tablename__ = "HelloWorld"

    uuid = database.Column(database.String(48), primary_key=True, default=uuid.uuid4)
    name = database.Column(database.Unicode, nullable=False)
    created_at = database.Column(database.DateTime, nullable=False, default=datetime.now)
    updated_at = database.Column(database.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class Group(database.Model):
    __tablename__ = "Groups"

    group_uuid = database.Column(database.String(48), primary_key=True, default=uuid.uuid4)

    groupname = database.Column(database.String(48), unique=True, nullable=False)
    hashed_password = database.Column(database.Unicode, nullable=False)
    display_name = database.Column(database.Unicode, nullable=False)

    created_at = database.Column(database.DateTime, nullable=False, default=datetime.now)
    updated_at = database.Column(database.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class GroupUsers(database.Model):
    __tablename__ = "GroupUsers"

    group_uuid = database.Column(database.String(48), database.ForeignKey("Groups.group_uuid"), primary_key = True)
    user_uuid = database.Column(database.String(48), database.ForeignKey("Users.user_uuid"), primary_key = True)

class GroupAdministrators(database.Model):
    __tablename__ = "GroupAdministrators"

    group_uuid = database.Column(database.String(48), database.ForeignKey("Groups.group_uuid"), primary_key = True)
    user_uuid = database.Column(database.String(48), database.ForeignKey("Users.user_uuid"), primary_key = True)


class User(database.Model):
    __tablename__ ="Users"

    user_uuid = database.Column(database.String(48), primary_key=True, default=uuid.uuid4)

    username = database.Column(database.String(48), unique=True, nullable=False)
    hashed_password = database.Column(database.Unicode, nullable=False)
    display_name = database.Column(database.Unicode, nullable=False)

    created_at = database.Column(database.DateTime, nullable=False, default=datetime.now)
    updated_at = database.Column(database.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
