import os
import sys
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import importlib
import glob

# Tambahkan path agar ws_handlers bisa diimport
sys.path.append(os.path.join(os.path.dirname(__file__), 'ws_handlers'))

# Dynamic import semua handler
handler_dir = os.path.join(os.path.dirname(__file__), 'ws_handlers')
handler_files = glob.glob(os.path.join(handler_dir, 'ws_*.py'))
WS_HANDLER_MAP = {}
for file in handler_files:
    mod_name = os.path.splitext(os.path.basename(file))[0]
    mod = importlib.import_module(mod_name)
    for attr in dir(mod):
        if attr.startswith('handle_ws_'):
            msg_type = attr.replace('handle_ws_', '').upper()
            WS_HANDLER_MAP[msg_type] = getattr(mod, attr)


app = FastAPI(title="AI-FRSS Modular WebSocket API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Import WebSocket routers (MVC refined)
from api.v1 import users_ws, roles_ws, alerts_ws, auth_ws, monitoring_ws

# Register routers (WebSocket endpoints)
app.include_router(users_ws.router, prefix="/ws/users", tags=["Users WS"])
app.include_router(roles_ws.router, prefix="/ws/roles", tags=["Roles WS"])
app.include_router(alerts_ws.router, prefix="/ws/alerts", tags=["Alerts WS"])
app.include_router(auth_ws.router, prefix="/ws/auth", tags=["Auth WS"])
app.include_router(monitoring_ws.router, prefix="/ws/monitoring", tags=["Monitoring WS"])
