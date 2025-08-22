from sqlalchemy import Column, Integer, ForeignKey
from .database import Base

class AssetTag(Base):
    __tablename__ = "assettags"

    id_asset = Column(Integer, ForeignKey("assets.id_asset", ondelete="CASCADE"), primary_key=True)
    id_tag = Column(Integer, ForeignKey("tags.id_tag", ondelete="CASCADE"), primary_key=True)
