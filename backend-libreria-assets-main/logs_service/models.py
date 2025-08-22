# backend-libreria-assets-main/logs_service/models.py

from sqlalchemy import Column, Integer, String, TIMESTAMP, text, Text
from .database import Base

class Log(Base):
    __tablename__ = "logs"

    id_log = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, nullable=True)
    id_asset = Column(Integer, nullable=True)
    id_categoria = Column(Integer, nullable=True)
    id_tag = Column(Integer, nullable=True)
    id_usuario_afectado = Column(Integer, nullable=True)
    accion = Column(String(100), nullable=False)
    valores_antes = Column(Text, nullable=True)
    valores_despues = Column(Text, nullable=True)
    entidad = Column(String(50), nullable=True)

    # Usamos text("CURRENT_TIMESTAMP") para que no se añadan comillas
    fecha_registro = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )
