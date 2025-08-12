import json
from models.camera import Camera
from services.db import get_db
from sqlalchemy.future import select

async def handle_monitoring_ws_event(data: str) -> str:
    payload = json.loads(data)
    action = payload.get("action")
    if action in ("get_feeds", "get_cameras"):
        async for db in get_db():
            result = await db.execute(select(Camera))
            cameras = result.scalars().all()
            cameras_data = [
                {"id": c.id, "name": c.name, "location": c.location, "status": c.status, "stream_url": c.stream_url}
                for c in cameras
            ]
            return json.dumps({"status": "success", "cameras": cameras_data})
    elif action == "get_streams":
        async for db in get_db():
            result = await db.execute(select(Camera))
            cameras = result.scalars().all()
            streams = [
                {"id": c.id, "url": c.stream_url}
                for c in cameras if c.stream_url
            ]
            return json.dumps({"status": "success", "streams": streams})
    elif action == "get_recordings":
        # TODO: Implement logic to fetch recordings (dummy)
        return json.dumps({"status": "success", "recordings": [
            {"id": 1, "filename": "rec1.mp4", "date": "2025-08-12"},
            {"id": 2, "filename": "rec2.mp4", "date": "2025-08-12"}
        ]})
    elif action == "get_recording_file":
        filename = payload.get("filename")
        # TODO: Implement logic to fetch file content or URL (dummy)
        return json.dumps({"status": "success", "file": {"filename": filename, "url": f"/media/{filename}"}})
    else:
        return json.dumps({"status": "error", "message": "Unknown action"})
