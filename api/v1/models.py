from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, String, Unicode, ForeignKey
from sqlalchemy.orm import relationship

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

    members = relationship("User", secondary="GroupUsers", back_populates="groups")
    administrators = relationship("User", secondary="GroupAdministrators", back_populates="administrated_groups")

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
class GroupUser(Base):
    __tablename__ = "GroupUsers"

    group_uuid = Column(String(48), ForeignKey("Groups.group_uuid"), primary_key = True)
    user_uuid = Column(String(48), ForeignKey("Users.user_uuid"), primary_key = True)

class GroupAdministrator(Base):
    __tablename__ = "GroupAdministrators"

    group_uuid = Column(String(48), ForeignKey("Groups.group_uuid"), primary_key = True)
    user_uuid = Column(String(48), ForeignKey("Users.user_uuid"), primary_key = True)

class User(Base):
    __tablename__ ="Users"

    user_uuid = Column(String(48), primary_key=True, default=uuid.uuid4)

    username = Column(String(48), unique=True, nullable=False)
    hashed_password = Column(Unicode, nullable=False)
    display_name = Column(Unicode, nullable=False)

    groups = relationship("Group", secondary="GroupUsers", back_populates="members")
    administrated_groups = relationship("Group", secondary="GroupAdministrators", back_populates="administrators")

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

