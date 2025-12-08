from datetime import datetime
from sqlalchemy.orm import Session

from app.models.presupuesto import Presupuesto
from app.schemas.presupuesto import PresupuestoCrear, PresupuestoActualizar


def crear_presupuesto(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    datos: PresupuestoCrear,
):
    pres = Presupuesto(
        empresa_id=empresa_id,
        nombre=datos.nombre,
        anio=datos.anio,
        periodo=datos.periodo,
        descripcion=datos.descripcion,
        estado=datos.estado,
        creado_por=usuario_id,
        creado_en=datetime.utcnow(),
    )
    db.add(pres)
    db.commit()
    db.refresh(pres)
    return pres


def listar_presupuestos(
    db: Session,
    empresa_id: int,
    anio: int | None = None,
    estado: str | None = None,
):
    q = db.query(Presupuesto).filter(Presupuesto.empresa_id == empresa_id)
    if anio is not None:
        q = q.filter(Presupuesto.anio == anio)
    if estado is not None:
        q = q.filter(Presupuesto.estado == estado)
    return q.order_by(Presupuesto.anio.desc(), Presupuesto.nombre).all()


def obtener_presupuesto(
    db: Session,
    empresa_id: int,
    presupuesto_id: int,
):
    return (
        db.query(Presupuesto)
        .filter(
            Presupuesto.empresa_id == empresa_id,
            Presupuesto.presupuesto_id == presupuesto_id,
        )
        .first()
    )


def actualizar_presupuesto(
    db: Session,
    empresa_id: int,
    presupuesto_id: int,
    usuario_id: int,
    datos: PresupuestoActualizar,
):
    pres = obtener_presupuesto(db, empresa_id, presupuesto_id)
    if not pres:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(pres, campo, valor)

    pres.actualizado_por = usuario_id
    pres.actualizado_en = datetime.utcnow()

    db.commit()
    db.refresh(pres)
    return pres
