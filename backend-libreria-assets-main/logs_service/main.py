from fastapi import FastAPI, Depends, HTTPException, status, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import logging
from .logging_config import setup_logging
import time
import asyncio

from . import schemas, crud, models
from .database import SessionLocal, engine, get_db

# Crea la tabla logs (ya sin FK) si no existe
models.Base.metadata.create_all(bind=engine)

# Initialize logging
logger = setup_logging("logs_service")

app = FastAPI(title="Logs Service")

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket manager para logs en tiempo real
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

@app.websocket("/ws/logs")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Mantener la conexión viva
    except WebSocketDisconnect:
        manager.disconnect(websocket)

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

@app.post("/", response_model=schemas.LogOut)
def create_log_endpoint(log_in: schemas.LogCreate, db: Session = Depends(get_db)):
    try:
        log = crud.create_log(db, log_in, log_in.id_usuario)
        # Enviar el log a todos los clientes conectados por WebSocket
        asyncio.create_task(manager.broadcast(schemas.LogOut.model_validate(log).__dict__))
        return log
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/", response_model=List[schemas.LogOut])
def read_logs(db: Session = Depends(get_db)):
    return crud.get_logs(db)
