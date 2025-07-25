from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
import uuid
from sqlalchemy.dialects.postgresql import UUID

# Create Base here for migration compatibility
Base = declarative_base()

class User(Base):
 """User model untuk authentication"""
 __tablename__ = "users"
 
 id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
 username = Column(String(50), unique=True, index=True, nullable=False)
 email = Column(String(100), unique=True, index=True, nullable=False)
 hashed_password = Column(String(255), nullable=False)
 full_name = Column(String(100), nullable=True)
 is_active = Column(Boolean, default=True)
 is_admin = Column(Boolean, default=False)
 created_at = Column(DateTime(timezone=True), server_default=func.now())
 updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class DetectionLog(Base):
 """Log untuk YOLO detections"""
 __tablename__ = "detection_logs"
 
 id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
 model_name = Column(String(50), nullable=False, index=True)
 image_path = Column(String(500), nullable=True)
 detections = Column(JSON, nullable=False) # Store detection results as JSON
 confidence_threshold = Column(Float, default=0.5)
 detection_count = Column(Integer, default=0)
 processing_time = Column(Float, nullable=True) # in seconds
 camera_id = Column(String(100), nullable=True, index=True)
 location = Column(String(200), nullable=True)
 created_at = Column(DateTime(timezone=True), server_default=func.now())

class Camera(Base):
 """Camera configuration"""
 __tablename__ = "cameras"
 
 id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
 name = Column(String(100), nullable=False)
 location = Column(String(200), nullable=False)
 ip_address = Column(String(45), nullable=True) # Support IPv6
 rtsp_url = Column(String(500), nullable=True)
 is_active = Column(Boolean, default=True)
 model_config = Column(JSON, nullable=True) # YOLO model settings
 created_at = Column(DateTime(timezone=True), server_default=func.now())
 updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Alert(Base):
 """Security alerts"""
 __tablename__ = "alerts"
 
 id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
 alert_type = Column(String(50), nullable=False, index=True) # intrusion, weapon, etc
 severity = Column(String(20), default="medium") # low, medium, high, critical
 message = Column(Text, nullable=False)
 camera_id = Column(String(100), nullable=True, index=True)
 location = Column(String(200), nullable=True)
 detection_data = Column(JSON, nullable=True) # Related detection info
 is_resolved = Column(Boolean, default=False)
 resolved_by = Column(String(100), nullable=True)
 resolved_at = Column(DateTime(timezone=True), nullable=True)
 created_at = Column(DateTime(timezone=True), server_default=func.now())

class SystemConfig(Base):
 """System configuration"""
 __tablename__ = "system_config"
 
 id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
 config_key = Column(String(100), unique=True, nullable=False, index=True)
 config_value = Column(JSON, nullable=False)
 description = Column(Text, nullable=True)
 created_at = Column(DateTime(timezone=True), server_default=func.now())
 updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Admin(Base):
 """Admin model untuk backward compatibility"""
 __tablename__ = "admin"
 
 id = Column(Integer, primary_key=True, index=True)
 username = Column(String(50), unique=True, index=True, nullable=False)
 password = Column(String(255), nullable=False)
 created_at = Column(DateTime(timezone=True), server_default=func.now())

class Face(Base):
 """Face recognition model"""
 __tablename__ = "faces"
 
 id = Column(Integer, primary_key=True, index=True)
 name = Column(String(100), nullable=False)
 embedding = Column(Text, nullable=False) # Store as comma-separated values
 created_at = Column(DateTime(timezone=True), server_default=func.now())
 updated_at = Column(DateTime(timezone=True), onupdate=func.now())
