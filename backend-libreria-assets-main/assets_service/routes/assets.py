# assets_service/routes/assets.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, crud
from ..database import get_db
import json

router = APIRouter()

@router.get("/", response_model=List[schemas.AssetOut])
def read_assets(
    category: Optional[int] = Query(None, description="Filtrar por id_categoria"),
    tag: Optional[int] = Query(None, description="Filtrar por id_tag"),
    db: Session = Depends(get_db)
):
    return crud.get_assets_filtered(db, category_id=category, tag_id=tag)

@router.post("/", response_model=schemas.AssetOut)
async def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    # Crear el asset
    nuevo_asset = crud.create_asset(db=db, asset=asset)
    
    # Registrar log con valores después del cambio
    valores_despues = {
        "nombre": nuevo_asset.nombre,
        "descripcion": nuevo_asset.descripcion,
        "url_imagen": nuevo_asset.url_imagen,
        "id_categoria": nuevo_asset.id_categoria
    }
    
    await crud.register_log_in_db(
        accion="create_asset",
        id_asset=int(getattr(nuevo_asset, 'id_asset', 0)),
        valores_despues=valores_despues
    )
    
    return nuevo_asset

@router.put("/{asset_id}", response_model=schemas.AssetOut)
async def update_asset(asset_id: int, asset_update: schemas.AssetUpdate, db: Session = Depends(get_db)):
    # Actualizar el asset y obtener valores anteriores
    result = crud.update_asset(db=db, asset_id=asset_id, asset_update=asset_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Asset no encontrado")
    
    updated_asset, valores_antes = result
    
    # Preparar valores después del cambio
    valores_despues = {
        "nombre": updated_asset.nombre,
        "descripcion": updated_asset.descripcion,
        "url_imagen": updated_asset.url_imagen,
        "id_categoria": updated_asset.id_categoria
    }
    
    # Registrar log con valores antes y después
    await crud.register_log_in_db(
        accion="update_asset",
        id_asset=int(getattr(updated_asset, 'id_asset', 0)),
        valores_antes=valores_antes,
        valores_despues=valores_despues
    )
    
    return updated_asset

@router.delete("/{asset_id}")
async def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    # Eliminar el asset y obtener valores anteriores
    valores_antes = crud.delete_asset(db=db, asset_id=asset_id)
    if valores_antes is None:
        raise HTTPException(status_code=404, detail="Asset no encontrado")
    
    # Registrar log con valores antes del cambio
    await crud.register_log_in_db(
        accion="delete_asset",
        id_asset=asset_id,
        valores_antes=valores_antes
    )
    
    return {"message": "Asset deleted"}
