
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio

import users_service.main       as users_app
import categories_service.main  as categories_app
import tags_service.main        as tags_app
import assets_service.main      as assets_app
import assettags_service.main   as assettags_app
import logs_service.main        as logs_app


# Socket.IO server (ASGI)
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=origins)
app = FastAPI(title="API Gateway - Librería de Imágenes")

# Estado de imágenes bloqueadas: { asset_id: sid }
locked_assets = {}

origins = ["*"]  # Allow all origins for development; change to specific origins in production


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.IO event handlers
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
    asset_id = data.get("asset_id")
    if asset_id is None:
        return
    if asset_id in locked_assets:
        # Ya está bloqueada
        await sio.emit("asset_locked", {"asset_id": asset_id, "locked": True}, room=sid)
    else:
        locked_assets[asset_id] = sid
        await sio.emit("asset_locked", {"asset_id": asset_id, "locked": True})

@sio.event
async def unlock_asset(sid, data):
    asset_id = data.get("asset_id")
    if asset_id is None:
        return
    if locked_assets.get(asset_id) == sid:
        del locked_assets[asset_id]
        await sio.emit("asset_unlocked", {"asset_id": asset_id})

# Montaje de microservicios REST bajo /api/…
app.mount("/api/users", users_app.app)
app.mount("/api/categories", categories_app.app)
app.mount("/api/tags", tags_app.app)
app.mount("/api/assets", assets_app.app)
app.mount("/api/assettags", assettags_app.app)
app.mount("/api/logs", logs_app.app)

# --------------------------------------------------------
# Montaje de archivos estáticos de Assets Service:
# todo /images → será atendido por assets_app (StaticFiles)
# --------------------------------------------------------
app.mount("/images", assets_app.app)

# Montar Socket.IO como ASGI app
from starlette.middleware import Middleware
from starlette.applications import Starlette
from starlette.routing import Mount

sio_app = socketio.ASGIApp(sio, app)



@app.get("/")
def root():
    return {"message": "Bienvenido al API Gateway de la Librería de Imágenes"}
