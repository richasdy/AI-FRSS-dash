from fastapi import APIRouter, HTTPException
from app.controller.auth_controller import sign_up_admin_http, login_admin_http
from app.schemas.auth_schemas import AdminSignUp, AdminLogin

router = APIRouter()

@router.post("/signup")
async def signup(data: AdminSignUp):
    return await sign_up_admin_http(data)

@router.post("/login")
async def login(data: AdminLogin):
    return await login_admin_http(data)
