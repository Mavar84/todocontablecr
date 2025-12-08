from datetime import datetime
from sqlalchemy.orm import Session
from app.models.bodega import Bodega
from app.schemas.bodega import BodegaCrear, BodegaActualizar


def crear_bodega(db: Session, datos: BodegaCrear, empresa_id: int, usuario_id: int):
    nueva = Bodega(
        empresa_id=empresa_id,
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        activo=datos.activo,
        created_by=usuario_id,
        created_at=datetime.utcnow(),
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def listar_bodegas(db: Session, empresa_id: int):
    return (
        db.query(Bodega)
        .filter(Bodega.empresa_id == empresa_id)
        .order_by(Bodega.nombre)
        .all()
    )


def obtener_bodega(db: Session, empresa_id: int, bodega_id: int):
    return (
        db.query(Bodega)
        .filter(
            Bodega.empresa_id == empresa_id,
            Bodega.bodega_id == bodega_id,
        )
        .first()
    )


def actualizar_bodega(db: Session, empresa_id: int, bodega_id: int, datos: BodegaActualizar, usuario_id: int):
    bodega = obtener_bodega(db, empresa_id, bodega_id)
    if not bodega:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(bodega, campo, valor)

    bodega.updated_by = usuario_id
    bodega.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(bodega)
    return bodega
