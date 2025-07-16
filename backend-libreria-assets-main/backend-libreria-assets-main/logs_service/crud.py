from sqlalchemy.orm import Session
from . import models, schemas

def create_log(db: Session, log_in: schemas.LogCreate, user_id: int | None):
    db_log = models.Log(
        id_usuario=user_id,
        id_asset=log_in.id_asset,
        id_categoria=log_in.id_categoria,
        id_tag=log_in.id_tag,
        id_usuario_afectado=log_in.id_usuario_afectado,
        accion=log_in.accion,
        valores_antes=log_in.valores_antes,
        valores_despues=log_in.valores_despues,
        entidad=log_in.entidad,
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_logs(db: Session):
    return db.query(models.Log).order_by(models.Log.fecha_registro.desc()).all()
