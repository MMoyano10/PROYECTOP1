# server.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import socketio

from typing import Dict

# Importa los apps que definiste en cada microservicio
from assets_service.main import app as assets_app
from tags_service.main import app as tags_app
from categories_service.main import app as categories_app
from users_service.main import app as users_app
from logs_service.main import app as logs_app

app = FastAPI()

# Socket.IO server (ASGI) para locks de imágenes y eventos en tiempo real
# Permitir orígenes del frontend en desarrollo
frontend_origins = [
    "http://localhost:4173",
    "http://127.0.0.1:4173",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=frontend_origins)

# Estado de imágenes bloqueadas: { asset_id: sid }
locked_assets: Dict[int, str] = {}

# Habilitar CORS global para el gateway
app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────── Montar carpeta estática ───────────────
# Esto sirve TODO lo que esté dentro de assets_service/static
# bajo la URL /static.
#
# Entonces, si en disco existe:
#   assets_service/static/images/laptop.jpg
# podrás acceder en el navegador a:
#   http://localhost:8000/static/images/laptop.jpg
#
# (Nota: la ruta “assets_service/static” es relativa a server.py)

app.mount(
    "/static",
    StaticFiles(directory="assets_service/static"),
    name="static"
)

# ─────────────── Montar microservicios ───────────────
# Cada uno de tus sub-apps (FastAPI) se monta bajo /api/...
app.mount("/api/assets", assets_app)
app.mount("/api/tags", tags_app)
app.mount("/api/categories", categories_app)
app.mount("/api/users", users_app)
app.mount("/api/logs", logs_app)

# ─────────────── Socket.IO events ───────────────

@sio.event
async def connect(sid, environ):
    print(f"Cliente conectado: {sid}")


@sio.event
async def disconnect(sid):
    print(f"Cliente desconectado: {sid}")
    # Liberar cualquier asset bloqueado por este cliente
    to_release = [aid for aid, owner in locked_assets.items() if owner == sid]
    for aid in to_release:
        del locked_assets[aid]
        await sio.emit("asset_unlocked", {"asset_id": aid})


@sio.event
async def lock_asset(sid, data):
    asset_id = data.get("asset_id") if isinstance(data, dict) else None
    if asset_id is None:
        return
    if asset_id in locked_assets:
        # Ya está bloqueada; notificar estado al solicitante
        await sio.emit("asset_locked", {"asset_id": asset_id, "locked": True}, room=sid)
    else:
        locked_assets[asset_id] = sid
        await sio.emit("asset_locked", {"asset_id": asset_id, "locked": True})


@sio.event
async def unlock_asset(sid, data):
    asset_id = data.get("asset_id") if isinstance(data, dict) else None
    if asset_id is None:
        return
    if locked_assets.get(asset_id) == sid:
        del locked_assets[asset_id]
        await sio.emit("asset_unlocked", {"asset_id": asset_id})


# Envolver FastAPI con Socket.IO para servir /socket.io
# Uvicorn seguirá usando "server:app"
app = socketio.ASGIApp(sio, app)
