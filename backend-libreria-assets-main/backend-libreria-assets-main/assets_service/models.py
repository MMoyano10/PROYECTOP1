# assets_service/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from .database import Base

# Tabla intermedia para relación muchos-a-muchos Asset <-> Tag
assettags = Table(
    'assettags',
    Base.metadata,
    Column('id_asset', Integer, ForeignKey('assets.id_asset', ondelete='CASCADE'), primary_key=True),
    Column('id_tag',   Integer, ForeignKey('tags.id_tag',   ondelete='CASCADE'), primary_key=True)
)

class Asset(Base):
    __tablename__ = "assets"

    id_asset    = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String(200), nullable=False)     # ej. "Laptop Gaming"
    descripcion = Column(Text, nullable=True)              # ej. "Laptop para gaming de alta gama"
    url_imagen  = Column(String(255), nullable=False)     # ej. "/static/images/laptop.jpg"
    id_categoria = Column(Integer, ForeignKey("categories.id_categoria"))

    # Relación con tags (muchos a muchos)
    tags = relationship("Tag", secondary=assettags, back_populates="assets")


class Tag(Base):
    __tablename__ = "tags"

    id_tag   = Column(Integer, primary_key=True, index=True)
    nombre   = Column(String(100), nullable=False, unique=True)

    assets = relationship("Asset", secondary=assettags, back_populates="tags")


class Category(Base):
    __tablename__ = "categories"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre       = Column(String(100), nullable=False)
