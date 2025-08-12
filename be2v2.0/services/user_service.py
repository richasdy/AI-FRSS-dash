import json
from models.user import User
from services.db import get_db
from sqlalchemy.future import select

async def handle_user_ws_event(data: str) -> str:
    payload = json.loads(data)
    action = payload.get("action")

    if action == "get_users":
        async for db in get_db():
            result = await db.execute(select(User))
            users = result.scalars().all()
            users_data = [
                {"id": u.id, "fullname": u.fullname, "email": u.email, "roleId": u.roleId}
                for u in users
            ]
            return json.dumps({"status": "success", "users": users_data})
    elif action == "create_user":
        # TODO: Implement create user logic
        return json.dumps({"status": "success", "message": "User created"})
    elif action == "get_user":
        # TODO: Implement get user logic
        return json.dumps({"status": "success", "data": {"id": 1, "name": "John"}})
    else:
        return json.dumps({"status": "error", "message": "Unknown action"})
