import json
from models.user import User
from services.db import get_db
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

async def handle_auth_ws_event(data: str) -> str:
    payload = json.loads(data)
    action = payload.get("action")
    if action == "signin":
        email = payload.get("email")
        password = payload.get("password")
        async for db in get_db():
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            if user and user.password == password:
                return json.dumps({"status": "success", "message": "Signed in", "user": {"id": user.id, "fullname": user.fullname, "email": user.email, "roleId": user.roleId}})
            else:
                return json.dumps({"status": "error", "message": "Invalid credentials"})
    elif action == "register":
        fullname = payload.get("fullname")
        email = payload.get("email")
        password = payload.get("password")
        roleId = payload.get("roleId")
        async for db in get_db():
            new_user = User(fullname=fullname, email=email, password=password, roleId=roleId)
            db.add(new_user)
            try:
                await db.commit()
                await db.refresh(new_user)
                return json.dumps({"status": "success", "message": "Registered", "user": {"id": new_user.id, "fullname": new_user.fullname, "email": new_user.email, "roleId": new_user.roleId}})
            except IntegrityError:
                await db.rollback()
                return json.dumps({"status": "error", "message": "Email already exists"})
    else:
        return json.dumps({"status": "error", "message": "Unknown action"})
