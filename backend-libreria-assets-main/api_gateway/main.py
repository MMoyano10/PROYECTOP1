from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

import users_service.main       as users_app
import categories_service.main  as categories_app
import tags_service.main        as tags_app
import assets_service.main      as assets_app
import assettags_service.main   as assettags_app
import logs_service.main        as logs_app

app = FastAPI(title="API Gateway - Librería de Imágenes")

# CORS: cuando allow_credentials=True, no se permite "*" como origen.
# Leemos FRONTEND_URL desde variables de entorno y hacemos fallback a localhost:4173.
frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:4173")
origins = [frontend_url, "http://127.0.0.1:4173", "http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Authorization"],
)

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


@app.get("/")
def root():
    return {"message": "Bienvenido al API Gateway de la Librería de Imágenes"}
