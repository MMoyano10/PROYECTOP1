from sqlalchemy.orm import Session
from . import models, schemas
import httpx
import json
from typing import Optional

# Obtener lista de tags, con opción de filtrar por categoría
def get_tags(db: Session, skip: int = 0, limit: int = 100, category: Optional[int] = None):
    query = db.query(models.Tag)
    if category is not None:
        query = query.join(models.Tag.assets).filter(models.Asset.id_categoria == category)
    return query.offset(skip).limit(limit).all()

# Obtener un tag por su ID
def get_tag(db: Session, id_tag: int):
    return db.query(models.Tag).filter(models.Tag.id_tag == id_tag).first()

# Crear un nuevo tag
def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(nombre=tag.nombre)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

# Actualizar un tag existente
def update_tag(db: Session, id_tag: int, tag_update: schemas.TagUpdate):
    db_tag = db.query(models.Tag).filter(models.Tag.id_tag == id_tag).first()
    if not db_tag:
        return None
    
    # Guardar valores antes del cambio
    old_values = {
        "nombre": db_tag.nombre
    }
    
    setattr(db_tag, 'nombre', tag_update.nombre)
    db.commit()
    db.refresh(db_tag)
    
    # Retornar tanto el tag actualizado como los valores anteriores
    return db_tag, old_values

# Eliminar un tag
def delete_tag(db: Session, id_tag: int):
    db_tag = db.query(models.Tag).filter(models.Tag.id_tag == id_tag).first()
    if not db_tag:
        return None
    
    # Guardar valores antes de eliminar
    old_values = {
        "nombre": db_tag.nombre
    }
    
    db.delete(db_tag)
    db.commit()
    
    return old_values

async def register_log_in_db(accion: str, user_id: Optional[int] = None, id_tag: Optional[int] = None, 
                           valores_antes: Optional[dict] = None, valores_despues: Optional[dict] = None):
    """Registra un log detallado en la base de datos a través del servicio de logs"""
    try:
        async with httpx.AsyncClient() as client:
            log_data = {
                "accion": accion,
                "id_usuario": user_id,
                "id_tag": id_tag,
                "valores_antes": json.dumps(valores_antes) if valores_antes else None,
                "valores_despues": json.dumps(valores_despues) if valores_despues else None,
                "entidad": "tag"
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
