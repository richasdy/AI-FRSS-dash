import json
from faces_controller import verify_face_handler, insert_face_handler
from auth_controller import sign_up_admin, login_admin

async def websocket_handler(websocket):
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)

            if msg.get("type") == "recognize_face":
                await verify_face_handler(websocket, msg)

            elif msg.get("type") == "insert_face":
                await insert_face_handler(websocket, msg)

            elif msg.get("type") == "insert_admin":
                await sign_up_admin(websocket, msg)

            elif msg.get("type") == "login":
                await login_admin(websocket, msg)

    except Exception as e:
        print("WebSocket error:", e)
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }
    )
)
