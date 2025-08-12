from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from . import Base

class Alert(Base):
    __tablename__ = "Alerts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    message = Column(Text)
    status = Column(String)
    createdAt = Column(DateTime, server_default=func.now())
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now())
