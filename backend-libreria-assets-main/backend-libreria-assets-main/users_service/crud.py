from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
import httpx
import json
from typing import Optional

# -------------------------------
#  Funciones auxiliares
# -------------------------------
def verify_password(plain_password: str, stored_password: str) -> bool:
    return plain_password == stored_password

# -------------------------------
#  CRUD: Usuarios
# -------------------------------
def get_user(db: Session, id_usuario: int):
    return db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def create_user(db: Session, user_in: schemas.UserCreate):
    db_user = models.Usuario(
        nombre=user_in.nombre,
        email=user_in.email,
        password=user_in.password,  # Guardamos la contraseña en texto plano
        is_admin=False  # Por defecto false; si quieres, se puede exponer en el payload
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise
    return db_user

def update_user(db: Session, id_usuario: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, id_usuario)
    if not db_user:
        return None

    # Guardar valores antes del cambio
    old_values = {
        "nombre": db_user.nombre,
        "email": db_user.email,
        "is_admin": db_user.is_admin
    }

    # Solo actualizamos campos si vienen en user_update
    if user_update.nombre is not None:
        db_user.nombre = user_update.nombre
    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.password is not None:
        db_user.password = user_update.password  # Guardamos la contraseña en texto plano
    if user_update.is_admin is not None:
        db_user.is_admin = user_update.is_admin

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Retornar tanto el usuario actualizado como los valores anteriores
    return db_user, old_values

def delete_user(db: Session, id_usuario: int):
    db_user = get_user(db, id_usuario)
    if not db_user:
        return None
    
    # Guardar valores antes de eliminar
    old_values = {
        "nombre": db_user.nombre,
        "email": db_user.email,
        "is_admin": db_user.is_admin
    }
    
    db.delete(db_user)
    db.commit()
    
    return old_values

async def register_log_in_db(accion: str, user_id: Optional[int] = None, id_usuario_afectado: Optional[int] = None, 
                           valores_antes: Optional[dict] = None, valores_despues: Optional[dict] = None):
    """Registra un log detallado en la base de datos a través del servicio de logs"""
    try:
        async with httpx.AsyncClient() as client:
            log_data = {
                "accion": accion,
                "id_usuario": user_id,
                "id_usuario_afectado": id_usuario_afectado,
                "valores_antes": json.dumps(valores_antes) if valores_antes else None,
                "valores_despues": json.dumps(valores_despues) if valores_despues else None,
                "entidad": "usuario"
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
