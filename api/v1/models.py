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
