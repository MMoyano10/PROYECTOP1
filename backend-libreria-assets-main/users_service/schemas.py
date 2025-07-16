from pydantic import BaseModel, EmailStr
from typing import Optional

# -------------------------------
# 1) Esquema base para usuario
#    (para crear usuarios completos)
# -------------------------------
class UserBase(BaseModel):
    nombre: str
    email: EmailStr
    password: str

class UserCreate(UserBase):
    """
    Se usa en el CRUD para crear nuevos usuarios.
    Requiere nombre, email y password.
    """
    pass

# -------------------------------
# 2) Esquema específico para login
#    (solo email y password)
# -------------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# -------------------------------
# 3) Esquema para respuesta de login con token
# -------------------------------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: 'UserOut'

# -------------------------------
# 4) Esquema para actualizar usuario
#    (todos los campos opcionales)
# -------------------------------
class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

# -------------------------------
# 5) Esquema de salida de usuario
#    (no incluye contraseña)
# -------------------------------
class UserOut(BaseModel):
    id_usuario: int
    nombre: str
    email: EmailStr
    is_admin: bool

    class Config:
        from_attributes = True
