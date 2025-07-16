from pydantic import BaseModel
from typing import Optional

class CategoryCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoryOut(BaseModel):
    id_categoria: int
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

class CategoryUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
