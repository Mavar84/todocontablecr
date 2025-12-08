from datetime import datetime
from sqlalchemy.orm import Session

from app.models.retencion_config import RetencionConfig
from app.schemas.retencion_config import RetencionConfigCrear, RetencionConfigActualizar


def crear_retencion_config(db: Session, empresa_id: int, datos: RetencionConfigCrear):
    nuevo = RetencionConfig(
        empresa_id=empresa_id,
        tipo=datos.tipo,
        nombre=datos.nombre,
        porcentaje=datos.porcentaje,
        base_minima=datos.base_minima,
        aplica_en_ventas=datos.aplica_en_ventas,
        aplica_en_compras=datos.aplica_en_compras,
        cuenta_retencion_id=datos.cuenta_retencion_id,
        activo=datos.activo,
        creado_en=datetime.utcnow(),
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_retenciones_config(db: Session, empresa_id: int, solo_activas: bool = True):
    q = db.query(RetencionConfig).filter(RetencionConfig.empresa_id == empresa_id)
    if solo_activas:
        q = q.filter(RetencionConfig.activo == True)
    return q.order_by(RetencionConfig.tipo, RetencionConfig.nombre).all()


def obtener_retencion_config(db: Session, empresa_id: int, retencion_config_id: int):
    return (
        db.query(RetencionConfig)
        .filter(
            RetencionConfig.empresa_id == empresa_id,
            RetencionConfig.retencion_config_id == retencion_config_id,
        )
        .first()
    )


def actualizar_retencion_config(db: Session, empresa_id: int, retencion_config_id: int, datos: RetencionConfigActualizar):
    rc = obtener_retencion_config(db, empresa_id, retencion_config_id)
    if not rc:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(rc, campo, valor)

    rc.actualizado_en = datetime.utcnow()
    db.commit()
    db.refresh(rc)
    return rc
