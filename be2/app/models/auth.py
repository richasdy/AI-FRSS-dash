"""
Authentication models
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.services.database_service import database_service

# Create declarative base
Base = declarative_base()

class User(Base):
    """User model for authentication"""
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

# Database operations for authentication
async def get_admin_by_username(username: str):
    """Get admin user by username"""
    try:
        query = "SELECT * FROM users WHERE username = :username AND is_admin = true"
        result = await database_service.fetch_one(query, {"username": username})
        return [result] if result else None
    except Exception as e:
        print(f"Error getting admin by username: {e}")
        return None

async def add_admin(username: str, password: str):
    """Add new admin user"""
    try:
        import bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        query = """
        INSERT INTO users (id, username, email, hashed_password, full_name, is_active, is_admin)
        VALUES (:id, :username, :email, :hashed_password, :full_name, :is_active, :is_admin)
        """
        values = {
            "id": str(uuid.uuid4()),
            "username": username,
            "email": f"{username}@admin.com",
            "hashed_password": hashed_password,
            "full_name": f"Admin {username}",
            "is_active": True,
            "is_admin": True
        }
        await database_service.execute_query(query, values)
        return True
    except Exception as e:
        print(f"Error adding admin: {e}")
        return False

# Export commonly used items
__all__ = ["User", "get_admin_by_username", "add_admin"]
