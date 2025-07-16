from fastapi import FastAPI, Depends, HTTPException, Header, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from starlette.status import HTTP_204_NO_CONTENT
import logging
from .logging_config import setup_logging
import time

from .database import SessionLocal, engine, Base
from . import crud, schemas, models

Base.metadata.create_all(bind=engine)
# Initialize logging
logger = setup_logging("tags_service")

app = FastAPI(title="Tags Service")

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1) LISTAR TAGS – público
@app.get("/", response_model=List[schemas.TagOut])
def list_tags(db: Session = Depends(get_db)):
    return crud.get_tags(db)

# 2) OBTENER TAG POR ID – público
@app.get("/{id_tag}", response_model=schemas.TagOut)
def get_tag_by_id(id_tag: int, db: Session = Depends(get_db)):
    db_tag = crud.get_tag(db, id_tag)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Etiqueta no encontrada")
    return db_tag

# 3) CREAR TAG – solo admin
@app.post("/", response_model=schemas.TagOut)
async def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    # Crear el tag
    nuevo_tag = crud.create_tag(db, tag)
    
    # Registrar log con valores después del cambio
    valores_despues = {
        "nombre": nuevo_tag.nombre
    }
    
    await crud.register_log_in_db(
        accion="create_tag",
        id_tag=int(getattr(nuevo_tag, 'id_tag', 0)),
        valores_despues=valores_despues
    )
    
    return nuevo_tag

# 4) ACTUALIZAR TAG – solo admin
@app.put("/{id_tag}", response_model=schemas.TagOut)
async def update_tag(id_tag: int, tag_update: schemas.TagUpdate, db: Session = Depends(get_db)):
    # Actualizar el tag y obtener valores anteriores
    result = crud.update_tag(db, id_tag, tag_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Tag no encontrado")
    
    updated_tag, valores_antes = result
    
    # Preparar valores después del cambio
    valores_despues = {
        "nombre": updated_tag.nombre
    }
    
    # Registrar log con valores antes y después
    await crud.register_log_in_db(
        accion="update_tag",
        id_tag=int(getattr(updated_tag, 'id_tag', 0)),
        valores_antes=valores_antes,
        valores_despues=valores_despues
    )
    
    return updated_tag

# 5) ELIMINAR TAG – solo admin
@app.delete("/{id_tag}", status_code=HTTP_204_NO_CONTENT)
async def delete_tag(id_tag: int, db: Session = Depends(get_db)):
    # Eliminar el tag y obtener valores anteriores
    valores_antes = crud.delete_tag(db, id_tag)
    if valores_antes is None:
        raise HTTPException(status_code=404, detail="Tag no encontrado")
    
    # Registrar log con valores antes del cambio
    await crud.register_log_in_db(
        accion="delete_tag",
        id_tag=id_tag,
        valores_antes=valores_antes
    )
    
    return
