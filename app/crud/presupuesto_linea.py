from datetime import datetime
from sqlalchemy.orm import Session

from app.models.presupuesto_linea import PresupuestoLinea
from app.models.presupuesto import Presupuesto
from app.schemas.presupuesto_linea import PresupuestoLineaCrear, PresupuestoLineaActualizar


def crear_presupuesto_linea(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    datos: PresupuestoLineaCrear,
):
    pres = (
        db.query(Presupuesto)
        .filter(
            Presupuesto.presupuesto_id == datos.presupuesto_id,
            Presupuesto.empresa_id == empresa_id,
        )
        .first()
    )
    if not pres:
        raise ValueError("Presupuesto no encontrado para esta empresa")

    linea = PresupuestoLinea(
        presupuesto_id=datos.presupuesto_id,
        empresa_id=empresa_id,
        cuenta_id=datos.cuenta_id,
        centro_costo_id=datos.centro_costo_id,
        mes=datos.mes,
        monto_presupuestado=datos.monto_presupuestado,
        comentario=datos.comentario,
        creado_por=usuario_id,
        creado_en=datetime.utcnow(),
    )
    db.add(linea)
    db.commit()
    db.refresh(linea)
    return linea


def listar_presupuesto_lineas(
    db: Session,
    empresa_id: int,
    presupuesto_id: int,
):
    return (
        db.query(PresupuestoLinea)
        .filter(
            PresupuestoLinea.empresa_id == empresa_id,
            PresupuestoLinea.presupuesto_id == presupuesto_id,
        )
        .order_by(PresupuestoLinea.cuenta_id, PresupuestoLinea.mes)
        .all()
    )


def obtener_presupuesto_linea(
    db: Session,
    empresa_id: int,
    linea_id: int,
):
    return (
        db.query(PresupuestoLinea)
        .filter(
            PresupuestoLinea.empresa_id == empresa_id,
            PresupuestoLinea.linea_id == linea_id,
        )
        .first()
    )


def actualizar_presupuesto_linea(
    db: Session,
    empresa_id: int,
    linea_id: int,
    usuario_id: int,
    datos: PresupuestoLineaActualizar,
):
    linea = obtener_presupuesto_linea(db, empresa_id, linea_id)
    if not linea:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(linea, campo, valor)

    linea.actualizado_por = usuario_id
    linea.actualizado_en = datetime.utcnow()

    db.commit()
    db.refresh(linea)
    return linea
