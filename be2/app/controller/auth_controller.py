import os
import json
import jwt
import bcrypt
from dotenv import load_dotenv
from models import auth as model_auth

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")

async def sign_up_admin(websocket, msg: dict):
    username = msg.get("username")
    password = msg.get("password")
    try:
        cek_user = await model_auth.get_admin_by_username(username)
        if cek_user:
            await websocket.send_text(json.dumps({
                "type": "insert_admin",
                "success": False,
                "message": "admin sudah terdaftar"
            }))
            return

        await model_auth.add_admin(username, password)
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
        found = await model_auth.get_admin_by_username(username)
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
