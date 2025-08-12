from fastapi import WebSocket

async def ws_users(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            # TODO: Implement logic to fetch/send users
            await websocket.send_json({
                "type": "users_response",
                "users": [],
                "message": "Users endpoint not implemented yet"
            })
    except Exception:
        await websocket.close()
