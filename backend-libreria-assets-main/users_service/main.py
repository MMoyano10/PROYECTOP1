from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging
from .logging_config import setup_logging
import time
import httpx
import asyncio
from typing import Optional
import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth

# IMPORTS RELATIVOS dentro del paquete users_service
from . import schemas, crud, models
from .database import SessionLocal, engine

# Configuración JWT
SECRET_KEY = os.environ.get("SESSION_SECRET", "change_me_in_prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configurar HTTPBearer para autenticación
security = HTTPBearer()

# Esto crea las tablas definidas en users_service/models.py
models.Base.metadata.create_all(bind=engine)

# Initialize logging
logger = setup_logging("users_service")

app = FastAPI(title="Users Service")

# Session middleware para OAuth
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, same_site="lax", https_only=False)

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    request_body = await request.body()
    logger.info({
        "event": "request",
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "body": request_body.decode(errors="replace")
    })
    try:
        response: Response = await call_next(request)
        process_time = time.time() - start_time
        logger.info({
            "event": "response",
            "status_code": response.status_code,
            "url": str(request.url),
            "process_time": process_time,
            "headers": dict(response.headers),
        })
        return response
    except Exception as e:
        logger.error({
            "event": "error",
            "url": str(request.url),
            "error": str(e)
        })
        raise


# -------------------------------
# Dependencia para sesión de DB
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
# Función helper para registrar logs en BD
# -------------------------------
async def register_log_in_db(accion: str, user_id: Optional[int] = None, id_asset: Optional[int] = None):
    """Registra un log en la base de datos a través del servicio de logs"""
    try:
        async with httpx.AsyncClient() as client:
            log_data = {
                "accion": accion,
                "id_usuario": user_id,
                "id_asset": id_asset
            }
            response = await client.post(
                "http://localhost:8000/api/logs/",
                json=log_data,
                timeout=5.0
            )
            if response.status_code == 200:
                logger.debug(f"Log registrado en BD: {accion}")
            else:
                logger.warning(f"Error al registrar log en BD: {response.status_code}")
    except Exception as e:
        logger.error(f"Error al conectar con servicio de logs: {str(e)}")


# -------------------------------
# Funciones JWT
# -------------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# -------------------------------
# Dependencia para obtener usuario actual desde token
# -------------------------------
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user = crud.get_user(db, int(user_id))
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    return user

# -------------------------------
# 1) Crear usuario (POST /)
# -------------------------------
@app.post("/", response_model=schemas.UserOut)
async def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    logger.info(f"Intento de creación de usuario iniciado para email: {user_in.email}")

    try:
        nuevo = crud.create_user(db, user_in)
        logger.info(f"Usuario creado exitosamente: {nuevo.nombre} (ID: {nuevo.id_usuario})")
        logger.debug(f"Detalles del usuario creado - Email: {nuevo.email}, Admin: {nuevo.is_admin}")
        
        # Registrar log con valores después del cambio
        valores_despues = {
            "nombre": nuevo.nombre,
            "email": nuevo.email,
            "is_admin": nuevo.is_admin
        }
        
        await crud.register_log_in_db(
            accion="create_user",
            id_usuario_afectado=int(nuevo.id_usuario),
            valores_despues=valores_despues
        )
        
        return nuevo
    except Exception as e:
        logger.error(f"Error al crear usuario con email {user_in.email}: {str(e)}")
        raise HTTPException(status_code=400, detail="Error al crear usuario (quizá email duplicado)")


# -------------------------------
# 2) Login de usuario (POST /login)
# -------------------------------
@app.post("/login", response_model=schemas.TokenResponse)
async def login_user(
    login_data: schemas.UserLogin,
    db: Session = Depends(get_db),
):
    logger.info(f"Intento de login iniciado para email: {login_data.email}")

    try:
        user = crud.get_user_by_email(db, login_data.email)
        if not user:
            logger.warning(f"Login fallido - Email no registrado: {login_data.email}")
            raise HTTPException(status_code=400, detail="Email no registrado")

        stored_password = getattr(user, "password", "")
        if not crud.verify_password(login_data.password, stored_password):
            logger.warning(f"Login fallido - Credenciales incorrectas para email: {login_data.email}")
            raise HTTPException(status_code=400, detail="Credenciales incorrectas")

        # Generar token JWT
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id_usuario)}, expires_delta=access_token_expires
        )

        logger.info(f"Login exitoso para usuario: {user.nombre} (ID: {user.id_usuario})")
        logger.debug(f"Detalles del login - Email: {login_data.email}, Usuario: {user.nombre}, Admin: {user.is_admin}")
        await register_log_in_db("login_user", user_id=int(user.id_usuario))

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }

    except HTTPException:
        # Re-lanzar HTTPException sin logging adicional
        raise
    except Exception as e:
        logger.error(f"Error inesperado durante login para email {login_data.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.options("/login")
async def options_login():
    return JSONResponse(content={}, status_code=200)

# -------------------------------
# 2.1) Verificar token (GET /me)
# -------------------------------
@app.get("/me", response_model=schemas.UserOut)
async def get_current_user_info(current_user = Depends(get_current_user)):
    return current_user

# -------------------------------
# 2.2) Logout de usuario (POST /logout)
# -------------------------------
@app.post("/logout")
async def logout_user(current_user = Depends(get_current_user)):
    logger.info(f"Logout de usuario: {current_user.nombre} (ID: {current_user.id_usuario})")
    await register_log_in_db("logout_user", user_id=int(current_user.id_usuario))
    return {"detail": "Sesión cerrada correctamente"}

# -------------------------------
# 3) Listar todos los usuarios (GET /)
# -------------------------------
@app.get("/", response_model=list[schemas.UserOut])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    logger.info(f"Solicitud de listado de usuarios - Skip: {skip}, Limit: {limit}")
    users = crud.get_users(db, skip=skip, limit=limit)
    logger.debug(f"Usuarios encontrados: {len(users)}")
    return users


# -------------------------------
# 4) Obtener usuario por ID (GET /{user_id})
# -------------------------------
@app.get("/{user_id}", response_model=schemas.UserOut)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
):
    logger.info(f"Solicitud de usuario por ID: {user_id}")
    user = crud.get_user(db, user_id)
    if not user:
        logger.warning(f"Usuario no encontrado con ID: {user_id}")
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    logger.debug(f"Usuario encontrado: {user.nombre} (ID: {user.id_usuario})")
    return user


# -------------------------------
# 5) Actualizar usuario (PUT /{user_id})
# -------------------------------
@app.put("/{user_id}", response_model=schemas.UserOut)
async def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
):
    logger.info(f"Solicitud de actualización de usuario ID: {user_id}")
    
    # Actualizar el usuario y obtener valores anteriores
    result = crud.update_user(db, user_id, user_update)
    if not result:
        logger.warning(f"Usuario no encontrado para actualizar con ID: {user_id}")
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    updated_user, valores_antes = result
    
    # Preparar valores después del cambio
    valores_despues = {
        "nombre": updated_user.nombre,
        "email": updated_user.email,
        "is_admin": updated_user.is_admin
    }
    
    logger.info(f"Usuario actualizado exitosamente: {updated_user.nombre} (ID: {updated_user.id_usuario})")
    
    # Registrar log con valores antes y después
    await crud.register_log_in_db(
        accion="update_user",
        id_usuario_afectado=int(updated_user.id_usuario),
        valores_antes=valores_antes,
        valores_despues=valores_despues
    )
    
    return updated_user


# -------------------------------
# 6) Eliminar usuario (DELETE /{user_id})
# -------------------------------
@app.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    logger.info(f"Solicitud de eliminación de usuario ID: {user_id}")
    
    # Eliminar el usuario y obtener valores anteriores
    valores_antes = crud.delete_user(db, user_id)
    if not valores_antes:
        logger.warning(f"Usuario no encontrado para eliminar con ID: {user_id}")
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    logger.info(f"Usuario eliminado exitosamente: {valores_antes['nombre']} (ID: {user_id})")
    
    # Registrar log con valores antes del cambio
    await crud.register_log_in_db(
        accion="delete_user",
        id_usuario_afectado=user_id,
        valores_antes=valores_antes
    )
    
    return {"detail": "Usuario eliminado correctamente"}

# ============================================
# Google OAuth 2.0 endpoints
# ============================================

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:4173")
BACKEND_GATEWAY_URL = os.environ.get("BACKEND_GATEWAY_URL", "http://localhost:8000")

oauth = OAuth()
if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    oauth.register(
        name="google",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

@app.get("/auth/google")
async def auth_google(request: Request):
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Faltan credenciales de Google")
    # Construir dinámicamente el redirect_uri usando el host real de la petición
    redirect_uri = str(request.url_for("auth_google_callback"))
    logger.info({"oauth": "google", "redirect_uri": redirect_uri})
    # Limpia estados antiguos para evitar que la cookie de sesión crezca y cause mismatch
    try:
        for k in list(request.session.keys()):
            if str(k).startswith("_state_google_"):
                request.session.pop(k, None)
    except Exception as e:
        logger.warning({"event": "oauth_cleanup_state_failed", "error": str(e)})
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/google/callback")
async def auth_google_callback(request: Request, db: Session = Depends(get_db)):
    # Intenta canjear el token; si hay mismatch de state, limpia y reintenta el flujo
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        logger.error({
            "event": "oauth_callback_error",
            "error": str(e)
        })
        # Limpiar estados antiguos y reiniciar el flujo para regenerar state/nonce
        try:
            for k in list(request.session.keys()):
                if str(k).startswith("_state_google_"):
                    request.session.pop(k, None)
        except Exception as ce:
            logger.warning({"event": "oauth_cleanup_state_failed", "error": str(ce)})
        # Redirige a iniciar OAuth nuevamente
        restart_url = str(request.url_for("auth_google"))
        return RedirectResponse(url=restart_url, status_code=302)
    userinfo = token.get("userinfo")
    if not userinfo:
        resp = await oauth.google.get("https://openidconnect.googleapis.com/v1/userinfo", token=token)
        userinfo = resp.json()
    email = userinfo.get("email")
    name = userinfo.get("name") or userinfo.get("given_name") or "Usuario"
    if not email:
        raise HTTPException(status_code=400, detail="No se pudo obtener el email del usuario")

    # Crear o recuperar usuario local
    user = crud.get_user_by_email(db, email)
    if not user:
        user = crud.create_user(db, schemas.UserCreate(nombre=name, email=email, password="oauth_google"))

    # Emitir JWT local
    access_token = create_access_token({"sub": str(user.id_usuario)})

    # Redirigir al frontend con token y datos básicos
    url = f"{FRONTEND_URL}/?token={access_token}&name={name}&email={email}"
    return RedirectResponse(url=url, status_code=302)
