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
logger = setup_logging("categories_service")

app = FastAPI(title="Categories Service")

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

# 1) LISTAR CATEGORÍAS – público
@app.get("/", response_model=List[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

# 2) OBTENER CATEGORÍA POR ID – público
@app.get("/{id_categoria}", response_model=schemas.CategoryOut)
def get_category_by_id(id_categoria: int, db: Session = Depends(get_db)):
    db_cat = crud.get_category(db, id_categoria)
    if not db_cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_cat

# 3) CREAR CATEGORÍA – solo admin
@app.post("/", response_model=schemas.CategoryOut)
async def create_category(cat: schemas.CategoryCreate, db: Session = Depends(get_db)):
    # Crear la categoría
    nueva_categoria = crud.create_category(db, cat)
    
    # Registrar log con valores después del cambio
    valores_despues = {
        "nombre": nueva_categoria.nombre,
        "descripcion": nueva_categoria.descripcion
    }
    
    await crud.register_log_in_db(
        accion="create_category",
        id_categoria=int(getattr(nueva_categoria, 'id_categoria', 0)),
        valores_despues=valores_despues
    )
    
    return nueva_categoria

# 4) ACTUALIZAR CATEGORÍA – solo admin
@app.put("/{id_categoria}", response_model=schemas.CategoryOut)
async def update_category(id_categoria: int, cat_update: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    # Actualizar la categoría y obtener valores anteriores
    result = crud.update_category(db, id_categoria, cat_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    updated_category, valores_antes = result
    
    # Preparar valores después del cambio
    valores_despues = {
        "nombre": updated_category.nombre,
        "descripcion": updated_category.descripcion
    }
    
    # Registrar log con valores antes y después
    await crud.register_log_in_db(
        accion="update_category",
        id_categoria=int(getattr(updated_category, 'id_categoria', 0)),
        valores_antes=valores_antes,
        valores_despues=valores_despues
    )
    
    return updated_category

# 5) ELIMINAR CATEGORÍA – solo admin
@app.delete("/{id_categoria}", status_code=HTTP_204_NO_CONTENT)
async def delete_category(id_categoria: int, db: Session = Depends(get_db)):
    # Eliminar la categoría y obtener valores anteriores
    valores_antes = crud.delete_category(db, id_categoria)
    if valores_antes is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Registrar log con valores antes del cambio
    await crud.register_log_in_db(
        accion="delete_category",
        id_categoria=id_categoria,
        valores_antes=valores_antes
    )
    
    return
