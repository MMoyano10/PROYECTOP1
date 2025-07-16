# backend-libreria-assets-main/tags_service/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración sin contraseña para el usuario root
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "mysql+pymysql://user:password@db:3306/libreria_assets"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
