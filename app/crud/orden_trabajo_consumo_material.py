from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.orden_trabajo import OrdenTrabajo
from app.models.orden_trabajo_consumo_material import OrdenTrabajoConsumoMaterial
from app.schemas.orden_trabajo_consumo_material import OrdenTrabajoConsumoMaterialCrear


def crear_consumo_material(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    datos: OrdenTrabajoConsumoMaterialCrear,
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

    costo_u = Decimal(str(datos.costo_unitario))
    cantidad = Decimal(str(datos.cantidad))
    costo_total = Decimal(str(datos.costo_total))

    if costo_total == 0:
        costo_total = costo_u * cantidad

    consumo = OrdenTrabajoConsumoMaterial(
        empresa_id=empresa_id,
        orden_trabajo_id=datos.orden_trabajo_id,
        producto_id=datos.producto_id,
        bodega_id=datos.bodega_id,
        fecha_consumo=datos.fecha_consumo,
        cantidad=cantidad,
        costo_unitario=costo_u,
        costo_total=costo_total,
        movimiento_inventario_id=datos.movimiento_inventario_id,
        comentario=datos.comentario,
        creado_por=usuario_id,
        creado_en=datetime.utcnow(),
    )
    db.add(consumo)
    db.commit()
    db.refresh(consumo)
    return consumo


def listar_consumos_material(
    db: Session,
    empresa_id: int,
    orden_trabajo_id: int,
):
    return (
        db.query(OrdenTrabajoConsumoMaterial)
        .filter(
            OrdenTrabajoConsumoMaterial.empresa_id == empresa_id,
            OrdenTrabajoConsumoMaterial.orden_trabajo_id == orden_trabajo_id,
        )
        .order_by(OrdenTrabajoConsumoMaterial.fecha_consumo)
        .all()
    )
