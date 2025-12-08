from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.orden_trabajo import OrdenTrabajo
from app.models.orden_trabajo_actividad import OrdenTrabajoActividad
from app.schemas.orden_trabajo_actividad import OrdenTrabajoActividadCrear


def crear_actividad_ot(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    datos: OrdenTrabajoActividadCrear,
):
    ot = (
        db.query(OrdenTrabajo)
        .filter(
            OrdenTrabajo.empresa_id == empresa_id,
            OrdenTrabajo.orden_trabajo_id == datos.orden_trabajo_id,
        )
        .first()
    )
    if not ot:
        raise ValueError("Orden de trabajo no encontrada para esta empresa")

    costo_mo = Decimal(str(datos.costo_mano_obra))
    horas = Decimal(str(datos.horas)) if datos.horas is not None else None
    tarifa = Decimal(str(datos.tarifa_hora)) if datos.tarifa_hora is not None else None

    if costo_mo == 0 and horas is not None and tarifa is not None:
        costo_mo = horas * tarifa

    actividad = OrdenTrabajoActividad(
        empresa_id=empresa_id,
        orden_trabajo_id=datos.orden_trabajo_id,
        fecha=datos.fecha,
        descripcion=datos.descripcion,
        horas=horas,
        tarifa_hora=tarifa,
        costo_mano_obra=costo_mo,
        costo_indirecto=datos.costo_indirecto,
        cuenta_contable_mo_id=datos.cuenta_contable_mo_id,
        cuenta_contable_indirectos_id=datos.cuenta_contable_indirectos_id,
        comentario=datos.comentario,
        creado_por=usuario_id,
        creado_en=datetime.utcnow(),
    )
    db.add(actividad)
    db.commit()
    db.refresh(actividad)
    return actividad


def listar_actividades_ot(
    db: Session,
    empresa_id: int,
    orden_trabajo_id: int,
):
    return (
        db.query(OrdenTrabajoActividad)
        .filter(
            OrdenTrabajoActividad.empresa_id == empresa_id,
            OrdenTrabajoActividad.orden_trabajo_id == orden_trabajo_id,
        )
        .order_by(OrdenTrabajoActividad.fecha)
        .all()
    )
