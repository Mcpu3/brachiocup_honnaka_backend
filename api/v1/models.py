from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, String, Unicode

from api.v1.database import Base


class HelloWorld(Base):
    __tablename__ = "HelloWorld"

    uuid = Column(String(48), primary_key=True, default=uuid.uuid4)
    name = Column(Unicode, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class Group(Base):
    __tablename__ = "Groups"

    group_uuid = Column(String(48), primary_key=True, default=uuid.uuid4)

    groupname = Column(String(48), unique=True, nullable=False)
    hashed_password = Column(Unicode, nullable=False)
    display_name = Column(Unicode, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
class User(Base):
    __tablename__ ="Users"

    user_uuid = Column(String(48), primary_key=True, default=uuid.uuid4)

    username = Column(String(48), unique=True, nullable=False)
    hashed_password = Column(Unicode, nullable=False)
    display_name = Column(Unicode, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)