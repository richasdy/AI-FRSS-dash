from fastapi import WebSocket

async def ws_roles(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            # TODO: Implement logic to fetch/send roles
            await websocket.send_json({
                "type": "roles_response",
                "roles": [],
                "message": "Roles endpoint not implemented yet"
            })
    except Exception:
        await websocket.close()
