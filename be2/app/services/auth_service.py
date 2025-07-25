"""
Unified Auth Service using SQLAlchemy ORM
"""
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from models.database_models import Admin
from services.database_service import DatabaseService

JWT_SECRET = os.getenv("JWT_SECRET", "default_secret")
db_service = DatabaseService()

class AuthService:
    """Unified Authentication Service"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def create_jwt_token(admin_data: Dict[str, Any]) -> str:
        """Create JWT token"""
        payload = {
            "id": admin_data["id"],
            "username": admin_data["username"],
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        return jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    
    @staticmethod
    async def get_admin_by_username(username: str) -> Optional[Admin]:
        """Get admin by username using SQLAlchemy"""
        async for session in db_service.get_session():
            stmt = select(Admin).where(Admin.username == username)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
    
    @staticmethod
    async def create_admin(username: str, password: str) -> Admin:
        """Create new admin using SQLAlchemy"""
        # Check if admin already exists
        existing = await AuthService.get_admin_by_username(username)
        if existing:
            raise HTTPException(status_code=400, detail="Admin already exists")
        
        async for session in db_service.get_session():
            # Create new admin
            hashed_password = AuthService.hash_password(password)
            new_admin = Admin(
                username=username,
                password=hashed_password,
                created_at=datetime.utcnow()
            )
            
            session.add(new_admin)
            await session.commit()
            await session.refresh(new_admin)
            return new_admin
    
    @staticmethod
    async def authenticate_admin(username: str, password: str) -> Dict[str, Any]:
        """Authenticate admin and return token"""
        admin = await AuthService.get_admin_by_username(username)
        if not admin:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not AuthService.verify_password(password, admin.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = AuthService.create_jwt_token({
            "id": admin.id,
            "username": admin.username
        })
        
        return {
            "type": "login",
            "success": True,
            "message": "Login successful",
            "token": token,
            "admin": {
                "id": admin.id,
                "username": admin.username
            }
        }

auth_service = AuthService()
