from sqlalchemy.orm import Session
from .models import Asset, Tag
from typing import List, Optional
import httpx
import asyncio
import json

def get_assets_filtered(db: Session, category_id: Optional[int], tag_id: Optional[int]) -> List[Asset]:
    query = db.query(Asset)
    if category_id:
        query = query.filter(Asset.id_categoria == category_id)
    if tag_id:
        query = query.filter(Asset.tags.any(Tag.id_tag == tag_id))
    return query.all()

def get_asset(db: Session, asset_id: int):
    return db.query(Asset).filter(Asset.id_asset == asset_id).first()

def create_asset(db: Session, asset):
    db_asset = Asset(
        nombre=asset.nombre,
        descripcion=asset.descripcion,
        url_imagen=asset.url_imagen,
        id_categoria=asset.id_categoria
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    # Handle tags assignment
    if hasattr(asset, 'tags') and asset.tags is not None:
        db_asset.tags = db.query(Tag).filter(Tag.id_tag.in_(asset.tags)).all()
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)
    return db_asset

def update_asset(db: Session, asset_id: int, asset_update):
    db_asset = get_asset(db, asset_id)
    if not db_asset:
        return None
    
    # Guardar valores antes del cambio
    old_values = {
        "nombre": db_asset.nombre,
        "descripcion": db_asset.descripcion,
        "url_imagen": db_asset.url_imagen,
        "id_categoria": db_asset.id_categoria
    }
    
    # Actualizar valores
    if asset_update.nombre is not None:
        db_asset.nombre = asset_update.nombre
    if asset_update.descripcion is not None:
        db_asset.descripcion = asset_update.descripcion
    if asset_update.url_imagen is not None:
        db_asset.url_imagen = asset_update.url_imagen
    if asset_update.id_categoria is not None:
        db_asset.id_categoria = asset_update.id_categoria
    # Handle tags assignment
    if hasattr(asset_update, 'tags') and asset_update.tags is not None:
        db_asset.tags = db.query(Tag).filter(Tag.id_tag.in_(asset_update.tags)).all()
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    
    # Retornar tanto el asset actualizado como los valores anteriores
    return db_asset, old_values

def delete_asset(db: Session, asset_id: int):
    db_asset = get_asset(db, asset_id)
    if not db_asset:
        return None
    
    # Guardar valores antes de eliminar
    old_values = {
        "nombre": db_asset.nombre,
        "descripcion": db_asset.descripcion,
        "url_imagen": db_asset.url_imagen,
        "id_categoria": db_asset.id_categoria
    }
    
    db.delete(db_asset)
    db.commit()
    
    return old_values

async def register_log_in_db(accion: str, user_id: Optional[int] = None, id_asset: Optional[int] = None, 
                           valores_antes: Optional[dict] = None, valores_despues: Optional[dict] = None):
    """Registra un log detallado en la base de datos a través del servicio de logs"""
    try:
        async with httpx.AsyncClient() as client:
            log_data = {
                "accion": accion,
                "id_usuario": user_id,
                "id_asset": id_asset,
                "valores_antes": json.dumps(valores_antes) if valores_antes else None,
                "valores_despues": json.dumps(valores_despues) if valores_despues else None,
                "entidad": "asset"
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
