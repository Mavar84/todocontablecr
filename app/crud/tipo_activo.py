from sqlalchemy.orm import Session
from datetime import datetime
from app.models.tipo_activo import TipoActivo
from app.schemas.tipo_activo import TipoActivoCrear, TipoActivoActualizar


def crear_tipo_activo(db: Session, datos: TipoActivoCrear, empresa_id: int, usuario_id: int):
    nuevo = TipoActivo(
        empresa_id=empresa_id,
        **datos.model_dump(),
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_tipos_activo(db: Session, empresa_id: int):
    return db.query(TipoActivo).filter(TipoActivo.empresa_id == empresa_id).all()


def obtener_tipo_activo(db: Session, empresa_id: int, tipo_activo_id: int):
    return (
        db.query(TipoActivo)
        .filter(
            TipoActivo.empresa_id == empresa_id,
            TipoActivo.tipo_activo_id == tipo_activo_id,
        )
        .first()
    )


def actualizar_tipo_activo(db: Session, empresa_id: int, tipo_activo_id: int, datos: TipoActivoActualizar):
    tipo = obtener_tipo_activo(db, empresa_id, tipo_activo_id)
    if not tipo:
        return None

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(tipo, campo, valor)

    db.commit()
    db.refresh(tipo)
    return tipo
