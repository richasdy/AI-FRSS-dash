from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from . import Base

class Camera(Base):
    __tablename__ = "Cameras"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String)
    status = Column(String)
    stream_url = Column(Text)
    createdAt = Column(DateTime, server_default=func.now())
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now())
