from pydantic import BaseModel
from typing import Optional, List


# Esquema base para reutilizar atributos comunes
class TagBase(BaseModel):
    nombre: str


# Esquema para crear un Tag (POST)
class TagCreate(TagBase):
    pass


# Esquema para actualizar un Tag (PUT)
class TagUpdate(TagBase):
    pass


# Esquema de salida con ID (GET)
class TagOut(TagBase):
    id_tag: int

    class Config:
        from_attributes = True
