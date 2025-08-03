import os
import json
import jwt
import bcrypt
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from dotenv import load_dotenv
from app.models.auth import get_admin_by_username, add_admin

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "default_secret")
security = HTTPBearer()

router = APIRouter(tags=["Authentication"])

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(request: LoginRequest):
    """Login endpoint for authentication"""
    try:
        user = await get_admin_by_username(request.username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify password (implement password verification logic)
        # This is a placeholder - implement proper password verification
        
        token = jwt.encode({"username": request.username}, JWT_SECRET, algorithm="HS256")
        return {
            "success": True,
            "token": token,
            "message": "Login successful"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register")
async def register(request: RegisterRequest):
    """Register admin endpoint"""
    try:
        existing_user = await get_admin_by_username(request.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Admin already registered")
        
        await add_admin(request.username, request.password)
        return {
            "success": True,
            "message": "Admin registered successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Legacy WebSocket functions (keeping for backward compatibility)
async def sign_up_admin(websocket, msg: dict):
    password = msg.get("password")
    try:
        cek_user = await get_admin_by_username(username)
        if cek_user:
            await websocket.send_text(json.dumps({
                "type": "insert_admin",
                "success": False,
                "message": "admin sudah terdaftar"
            }))
            return

        await add_admin(username, password)
        await websocket.send_text(json.dumps({
            "type": "insert_admin",
            "success": True,
            "message": "Admin registered successfully"
        }))
    except Exception as e:
        print(e)
        await websocket.send_text(json.dumps({
            "type": "insert_admin",
            "success": False,
            "message": str(e)
        }))

async def login_admin(websocket, msg: dict):
    username = msg.get("username")
    password = msg.get("password")
    try:
        found = await get_admin_by_username(username)
        if found:
            admin = found[0]
            if bcrypt.checkpw(password.encode('utf-8'), admin["password"].encode('utf-8')):
                token = jwt.encode({"id": admin["id"]}, JWT_SECRET, algorithm="HS256")
                await websocket.send_text(json.dumps({
                    "type": "login",
                    "success": True,
                    "message": "login successful",
                    "token": token
                }))
                return
        await websocket.send_text(json.dumps({
            "type": "login",
            "success": False,
            "message": "username or password is incorrect"
        }))
    except Exception as e:
        print(e)
        await websocket.send_text(json.dumps({
            "type": "login",
            "success": False,
            "message": str(e)
        }
    )
)
