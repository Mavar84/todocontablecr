from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal

from app.models.activo_fijo import ActivoFijo
from app.models.depreciacion_activo import DepreciacionActivo
from app.schemas.activo_fijo import ActivoFijoCrear, ActivoFijoActualizar
from app.schemas.depreciacion_activo import DepreciacionActivoCrear


def crear_activo_fijo(db: Session, datos: ActivoFijoCrear, empresa_id: int, usuario_id: int):
    activo = ActivoFijo(
        empresa_id=empresa_id,
        **datos.model_dump(),
        depreciacion_acumulada=0,
        valor_en_libros=datos.costo,
        created_by=usuario_id,
        created_at=datetime.utcnow(),
    )
    db.add(activo)
    db.commit()
    db.refresh(activo)
    return activo


def listar_activos(db: Session, empresa_id: int):
    return (
        db.query(ActivoFijo)
        .filter(ActivoFijo.empresa_id == empresa_id)
        .order_by(ActivoFijo.fecha_compra.desc())
        .all()
    )


def obtener_activo(db: Session, empresa_id: int, activo_id: int):
    return (
        db.query(ActivoFijo)
        .filter(
            ActivoFijo.empresa_id == empresa_id,
            ActivoFijo.activo_id == activo_id,
        )
        .first()
    )


def actualizar_activo(db: Session, empresa_id: int, activo_id: int, datos: ActivoFijoActualizar, usuario_id: int):
    activo = obtener_activo(db, empresa_id, activo_id)
    if not activo:
        return None

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(activo, campo, valor)

    activo.updated_by = usuario_id
    activo.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(activo)
    return activo
