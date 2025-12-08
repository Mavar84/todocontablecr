from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.orden_trabajo import OrdenTrabajo
from app.models.orden_trabajo_consumo_material import OrdenTrabajoConsumoMaterial
from app.models.orden_trabajo_actividad import OrdenTrabajoActividad
from app.schemas.orden_trabajo import OrdenTrabajoCrear, OrdenTrabajoActualizar


def crear_orden_trabajo(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    datos: OrdenTrabajoCrear,
):
    ot = OrdenTrabajo(
        empresa_id=empresa_id,
        codigo=datos.codigo,
        descripcion=datos.descripcion,
        producto_final_id=datos.producto_final_id,
        cantidad_planeada=datos.cantidad_planeada,
        cantidad_producida=datos.cantidad_producida,
        fecha_creacion=datos.fecha_creacion,
        fecha_inicio=datos.fecha_inicio,
        fecha_fin=datos.fecha_fin,
        estado=datos.estado,
        centro_costo_id=datos.centro_costo_id,
        bodega_origen_id=datos.bodega_origen_id,
        bodega_destino_id=datos.bodega_destino_id,
        costo_materiales=0,
        costo_mano_obra=0,
        costo_indirectos=0,
        costo_total=0,
        creado_por=usuario_id,
        creado_en=datetime.utcnow(),
    )
    db.add(ot)
    db.commit()
    db.refresh(ot)
    return ot


def listar_ordenes_trabajo(
    db: Session,
    empresa_id: int,
    estado: str | None = None,
    producto_final_id: int | None = None,
):
    q = db.query(OrdenTrabajo).filter(OrdenTrabajo.empresa_id == empresa_id)
    if estado:
        q = q.filter(OrdenTrabajo.estado == estado)
    if producto_final_id:
        q = q.filter(OrdenTrabajo.producto_final_id == producto_final_id)
    return q.order_by(OrdenTrabajo.fecha_creacion.desc(), OrdenTrabajo.orden_trabajo_id.desc()).all()


def obtener_orden_trabajo(
    db: Session,
    empresa_id: int,
    orden_trabajo_id: int,
):
    return (
        db.query(OrdenTrabajo)
        .filter(
            OrdenTrabajo.empresa_id == empresa_id,
            OrdenTrabajo.orden_trabajo_id == orden_trabajo_id,
        )
        .first()
    )


def actualizar_orden_trabajo(
    db: Session,
    empresa_id: int,
    orden_trabajo_id: int,
    usuario_id: int,
    datos: OrdenTrabajoActualizar,
):
    ot = obtener_orden_trabajo(db, empresa_id, orden_trabajo_id)
    if not ot:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(ot, campo, valor)

    ot.actualizado_por = usuario_id
    ot.actualizado_en = datetime.utcnow()

    db.commit()
    db.refresh(ot)
    return ot


def recalcular_costos_orden_trabajo(
    db: Session,
    empresa_id: int,
    orden_trabajo_id: int,
):
    ot = obtener_orden_trabajo(db, empresa_id, orden_trabajo_id)
    if not ot:
        raise ValueError("Orden de trabajo no encontrada")

    consumos = (
        db.query(OrdenTrabajoConsumoMaterial)
        .filter(
            OrdenTrabajoConsumoMaterial.empresa_id == empresa_id,
            OrdenTrabajoConsumoMaterial.orden_trabajo_id == orden_trabajo_id,
        )
        .all()
    )
    actividades = (
        db.query(OrdenTrabajoActividad)
        .filter(
            OrdenTrabajoActividad.empresa_id == empresa_id,
            OrdenTrabajoActividad.orden_trabajo_id == orden_trabajo_id,
        )
        .all()
    )

    costo_materiales = sum(Decimal(str(c.costo_total)) for c in consumos)
    costo_mano_obra = sum(Decimal(str(a.costo_mano_obra)) for a in actividades)
    costo_indirectos = sum(Decimal(str(a.costo_indirecto)) for a in actividades)

    ot.costo_materiales = costo_materiales
    ot.costo_mano_obra = costo_mano_obra
    ot.costo_indirectos = costo_indirectos
    ot.costo_total = costo_materiales + costo_mano_obra + costo_indirectos

    if ot.cantidad_producida and Decimal(str(ot.cantidad_producida)) > 0:
        ot.costo_unitario = ot.costo_total / Decimal(str(ot.cantidad_producida))
    else:
        ot.costo_unitario = None

    db.commit()
    db.refresh(ot)
    return ot
