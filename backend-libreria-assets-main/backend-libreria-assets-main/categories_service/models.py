from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Category(Base):
    __tablename__ = "categories"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre       = Column(String(100), unique=True, nullable=False)
    descripcion  = Column(Text, nullable=True)
