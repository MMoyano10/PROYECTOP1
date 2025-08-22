from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Tabla intermedia assettags
assettags = Table(
    "assettags",
    Base.metadata,
    Column("id_asset", ForeignKey("assets.id_asset"), primary_key=True),
    Column("id_tag", ForeignKey("tags.id_tag"), primary_key=True)
)

class Tag(Base):
    __tablename__ = "tags"

    id_tag = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    # Relación muchos a muchos con assets eliminada para microservicio independiente
