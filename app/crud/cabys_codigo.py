from datetime import datetime
from sqlalchemy.orm import Session

from app.models.cabys_codigo import CabysCodigo
from app.schemas.cabys_codigo import CabysCodigoCrear, CabysCodigoActualizar


def crear_cabys(db: Session, datos: CabysCodigoCrear):
    nuevo = CabysCodigo(
        codigo=datos.codigo,
        descripcion=datos.descripcion,
        activo=datos.activo,
        creado_en=datetime.utcnow(),
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_cabys(db: Session, solo_activos: bool = True):
    q = db.query(CabysCodigo)
    if solo_activos:
        q = q.filter(CabysCodigo.activo == True)
    return q.order_by(CabysCodigo.codigo).all()


def obtener_cabys(db: Session, cabys_id: int):
    return (
        db.query(CabysCodigo)
        .filter(CabysCodigo.cabys_id == cabys_id)
        .first()
    )


def buscar_cabys_por_codigo(db: Session, codigo: str):
    return (
        db.query(CabysCodigo)
        .filter(CabysCodigo.codigo == codigo)
        .first()
    )


def actualizar_cabys(db: Session, cabys_id: int, datos: CabysCodigoActualizar):
    cab = obtener_cabys(db, cabys_id)
    if not cab:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(cab, campo, valor)

    cab.actualizado_en = datetime.utcnow()
    db.commit()
    db.refresh(cab)
    return cab
