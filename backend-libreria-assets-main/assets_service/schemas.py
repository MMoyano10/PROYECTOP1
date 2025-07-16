from pydantic import BaseModel
from typing import List, Optional


class TagOut(BaseModel):
    id_tag: int
    nombre: str

    class Config:
        from_attributes = True


class AssetBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    url_imagen: str
    id_categoria: Optional[int] = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    url_imagen: Optional[str] = None
    id_categoria: Optional[int] = None


class AssetOut(AssetBase):
    id_asset: int
    #tags: List[TagOut] = []

    class Config:
        from_attributes = True
