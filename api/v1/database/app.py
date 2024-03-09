from datetime import datetime
import os
import urllib.parse
import uuid

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import functions

DATABASE_PASSWORD = ""
DATABASE_CONNECTION_STRING = urllib.parse.quote_plus("Driver={ODBC Driver 18 for SQL Server};Server=tcp:brachiocup-honnaka-backend.database.windows.net,1433;Database=brachiocup-honnaka-backend;Uid=brachiocup-honnaka-backend;Pwd={%s};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;" % DATABASE_PASSWORD)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc:///?odbc_connect={DATABASE_CONNECTION_STRING}"
database = SQLAlchemy(app)
migrate = Migrate(app, database)


class Helloworld(database.Model):
    __tablename__ = "Helloworld"

    uuid = database.Column(database.String(48), primary_key=True, default=uuid.uuid4)
    name = database.Column(database.String(48), nullable=True)
    created_at = database.Column(database.DateTime, nullable=False, default=datetime.now)
    updated_at = database.Column(database.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)