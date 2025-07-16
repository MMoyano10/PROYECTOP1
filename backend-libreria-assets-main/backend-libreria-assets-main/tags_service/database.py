# backend-libreria-assets-main/tags_service/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración sin contraseña para el usuario root
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    f"mysql+pymysql://{os.environ.get('DB_USER', 'user')}:{os.environ.get('DB_PASSWORD', 'password')}@{os.environ.get('DB_HOST', 'db')}:3306/{os.environ.get('DB_NAME', 'libreria_assets')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
