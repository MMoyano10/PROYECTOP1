from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LogCreate(BaseModel):
    id_usuario: Optional[int] = None
    id_asset: Optional[int] = None
    id_categoria: Optional[int] = None
    id_tag: Optional[int] = None
    id_usuario_afectado: Optional[int] = None
    accion: str
    valores_antes: Optional[str] = None
    valores_despues: Optional[str] = None
    entidad: Optional[str] = None

class LogOut(BaseModel):
    id_log: int
    id_usuario: Optional[int] = None
    id_asset: Optional[int] = None
    id_categoria: Optional[int] = None
    id_tag: Optional[int] = None
    id_usuario_afectado: Optional[int] = None
    accion: str
    valores_antes: Optional[str] = None
    valores_despues: Optional[str] = None
    entidad: Optional[str] = None
    fecha_registro: datetime

    class Config:
        from_attributes = True
