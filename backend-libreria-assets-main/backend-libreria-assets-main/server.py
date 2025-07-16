# server.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Importa los apps que definiste en cada microservicio
from assets_service.main import app as assets_app
from tags_service.main import app as tags_app
from categories_service.main import app as categories_app
from users_service.main import app as users_app
from logs_service.main import app as logs_app

app = FastAPI()

# Habilitar CORS global para el gateway
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # O ["*"] para pruebas
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
