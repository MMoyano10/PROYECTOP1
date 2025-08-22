# assets_service/main.py
from fastapi import FastAPI, Depends, Query, HTTPException, Request, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, crud
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from .routes import assets  # <-- tu archivo con las rutas
import logging
from .logging_config import setup_logging
import time
from fastapi.responses import JSONResponse

# Crear las tablas si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Initialize logging
logger = setup_logging("assets_service")

# Habilitar CORS
import os
frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:4173")
origins = [frontend_url, "http://127.0.0.1:4173", "http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Authorization"],
)

# Ruta de prueba para confirmar que el backend funciona
@app.get("/ping")
def ping():
    return {"message": "pong"}

# Servir archivos estáticos (imágenes)
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static"
)

# Dependencia para la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Incluir las rutas del servicio sin prefijo; el gateway las montará bajo /api/assets
app.include_router(assets.router)

@app.options("/login")
async def options_login():
    return JSONResponse(content={}, status_code=200)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    request_body = await request.body()
    logger.info({
        "event": "request",
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "body": request_body.decode(errors="replace")
    })
    try:
        response: Response = await call_next(request)
        process_time = time.time() - start_time
        logger.info({
            "event": "response",
            "status_code": response.status_code,
            "url": str(request.url),
            "process_time": process_time,
            "headers": dict(response.headers),
        })
        return response
    except Exception as e:
        logger.error({
            "event": "error",
            "url": str(request.url),
            "error": str(e)
        })
        raise
