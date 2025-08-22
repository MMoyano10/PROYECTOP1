from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
import httpx
import json
from typing import Optional

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_category(db: Session, id_categoria: int):
    return db.query(models.Category).filter(models.Category.id_categoria == id_categoria).first()

def create_category(db: Session, cat: schemas.CategoryCreate):
    # Verificar duplicado
    existing = db.query(models.Category).filter(models.Category.nombre == cat.nombre).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")
    db_cat = models.Category(
        nombre=cat.nombre,
        descripcion=cat.descripcion
    )
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def update_category(db: Session, id_categoria: int, cat_update: schemas.CategoryUpdate):
    db_cat = get_category(db, id_categoria)
    if not db_cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Guardar valores antes del cambio
    old_values = {
        "nombre": db_cat.nombre,
        "descripcion": db_cat.descripcion
    }
    
    # Si cambian nombre, revisar que no haya duplicado
    if cat_update.nombre and cat_update.nombre != db_cat.nombre:
        if db.query(models.Category).filter(models.Category.nombre == cat_update.nombre).first():
            raise HTTPException(status_code=400, detail="Ese nombre ya existe")
        db_cat.nombre = cat_update.nombre
    if cat_update.descripcion is not None:
        db_cat.descripcion = cat_update.descripcion
    
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    
    # Retornar tanto la categoría actualizada como los valores anteriores
    return db_cat, old_values

def delete_category(db: Session, id_categoria: int):
    db_cat = get_category(db, id_categoria)
    if not db_cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Guardar valores antes de eliminar
    old_values = {
        "nombre": db_cat.nombre,
        "descripcion": db_cat.descripcion
    }
    
    db.delete(db_cat)
    db.commit()
    
    return old_values

async def register_log_in_db(accion: str, user_id: Optional[int] = None, id_categoria: Optional[int] = None, 
                           valores_antes: Optional[dict] = None, valores_despues: Optional[dict] = None):
    """Registra un log detallado en la base de datos a través del servicio de logs"""
    try:
        async with httpx.AsyncClient() as client:
            log_data = {
                "accion": accion,
                "id_usuario": user_id,
                "id_categoria": id_categoria,
                "valores_antes": json.dumps(valores_antes) if valores_antes else None,
                "valores_despues": json.dumps(valores_despues) if valores_despues else None,
                "entidad": "categoria"
            }
            response = await client.post(
                "http://localhost:8000/api/logs/",
                json=log_data,
                timeout=5.0
            )
            if response.status_code == 200:
                print(f"Log registrado en BD: {accion}")
            else:
                print(f"Error al registrar log en BD: {response.status_code}")
    except Exception as e:
        print(f"Error al conectar con servicio de logs: {str(e)}")
