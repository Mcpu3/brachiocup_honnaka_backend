from datetime import datetime
import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Unicode, text
from sqlalchemy.sql import functions

from api.v1.database import Base


class Helloworld(Base):
    __tablename__ = "Helloworld"
   
    uuid = Column(String(48), primary_key=True, default=uuid.uuid4)
    name = Column(String(48), nullable=True)
    # created_at = Column(DateTime, nullable=False, server_default=functions.current_timestamp())
    # # updated_at = Column(DateTime, nullable=False, server_dafault=text("current_timestamp on update current_timestamp"))
    # updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)