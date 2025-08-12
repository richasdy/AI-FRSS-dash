
import json
from models.role import Role
from services.db import get_db
from sqlalchemy.future import select

async def handle_role_ws_event(data: str) -> str:
    payload = json.loads(data)
    action = payload.get("action")

    if action == "get_roles":
        # Query roles from DB
        async for db in get_db():
            result = await db.execute(select(Role))
            roles = result.scalars().all()
            roles_data = [
                {"id": r.id, "name": r.name, "description": r.description, "permissions": r.permissions}
                for r in roles
            ]
            return json.dumps({"status": "success", "roles": roles_data})
    else:
        return json.dumps({"status": "error", "message": "Unknown action"})
