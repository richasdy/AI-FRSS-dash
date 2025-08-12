import json
from models.alert import Alert
from services.db import get_db
from sqlalchemy.future import select

async def handle_alert_ws_event(data: str) -> str:
    payload = json.loads(data)
    action = payload.get("action")

    if action in ("get_alerts", "get_alert_history", "get_live_alerts"):
        async for db in get_db():
            result = await db.execute(select(Alert))
            alerts = result.scalars().all()
            alerts_data = [
                {"id": a.id, "type": a.type, "message": a.message, "status": a.status, "createdAt": str(a.createdAt)}
                for a in alerts
            ]
            return json.dumps({"status": "success", "alerts": alerts_data})
    else:
        return json.dumps({"status": "error", "message": "Unknown action"})
