import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración sin contraseña para el usuario root
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "mysql+pymysql://user:password@db:3306/libreria_assets"
)

# 1) Creamos el Engine de SQLAlchemy
engine = create_engine(DATABASE_URL)

# 2) Configuramos el SessionLocal (fábrica de sesiones)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 3) Declarative base que usarán todos los models
Base = declarative_base()

# 4) Generador de dependencias para FastAPI,
#    que abrirá y cerrará la sesión en cada request:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
