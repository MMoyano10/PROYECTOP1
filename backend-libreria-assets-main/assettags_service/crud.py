from sqlalchemy.orm import Session
from . import models, schemas

def create_assettag(db: Session, assettag: schemas.AssetTagCreate):
    db_assettag = models.AssetTag(**assettag.dict())
    db.add(db_assettag)
    db.commit()
    return db_assettag

def get_assettags(db: Session):
    return db.query(models.AssetTag).all()

def delete_assettag(db: Session, id_asset: int, id_tag: int):
    db_assettag = db.query(models.AssetTag).filter_by(id_asset=id_asset, id_tag=id_tag).first()
    if db_assettag:
        db.delete(db_assettag)
        db.commit()
        return True
    return False
