from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.orden_compra import OrdenCompra
from app.models.orden_compra_detalle import OrdenCompraDetalle
from app.schemas.orden_compra import OrdenCompraCreate


def _dec(value: float | None) -> Decimal:
    if value is None:
        return Decimal("0.00")
    return Decimal(str(value))


def crear_orden_compra(
    db: Session,
    data: OrdenCompraCreate,
    empresa_id: int,
    usuario_id: int,
):
    if not data.detalles or len(data.detalles) == 0:
        raise ValueError("La orden de compra debe tener al menos una línea")

    subtotal = Decimal("0.00")
    descuento_total = Decimal("0.00")
    impuesto_total = Decimal("0.00")

    for det in data.detalles:
        cantidad = _dec(det.cantidad)
        costo = _dec(det.costo_unitario)
        desc = _dec(det.descuento)
        imp = _dec(det.impuesto)

        linea_bruta = cantidad * costo
        subtotal += linea_bruta
        descuento_total += desc
        impuesto_total += imp

    total = subtotal - descuento_total + impuesto_total

    nueva = OrdenCompra(
        empresa_id=empresa_id,
        proveedor_id=data.proveedor_id,
        numero=data.numero,
        fecha=data.fecha,
        moneda_id=data.moneda_id,
        subtotal=subtotal,
        descuento_total=descuento_total,
        impuesto_total=impuesto_total,
        total=total,
        estado="aprobada",
        bodega_entrada_id=data.bodega_entrada_id,
        created_by=usuario_id,
        created_at=datetime.utcnow(),
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    for det in data.detalles:
        cantidad = _dec(det.cantidad)
        costo = _dec(det.costo_unitario)
        desc = _dec(det.descuento)
        imp = _dec(det.impuesto)
        linea_bruta = cantidad * costo
        total_linea = linea_bruta - desc + imp

        nuevo_det = OrdenCompraDetalle(
            orden_compra_id=nueva.orden_compra_id,
            producto_id=det.producto_id,
            descripcion=det.descripcion,
            cantidad=cantidad,
            costo_unitario=costo,
            descuento=desc,
            impuesto=imp,
            total_linea=total_linea,
            cuenta_gasto_id=det.cuenta_gasto_id,
        )
        db.add(nuevo_det)

    db.commit()
    db.refresh(nueva)
    return nueva


def listar_ordenes_compra(db: Session, empresa_id: int):
    return (
        db.query(OrdenCompra)
        .filter(OrdenCompra.empresa_id == empresa_id)
        .order_by(OrdenCompra.fecha.desc(), OrdenCompra.orden_compra_id.desc())
        .all()
    )


def obtener_orden_compra(db: Session, empresa_id: int, orden_compra_id: int):
    return (
        db.query(OrdenCompra)
        .filter(
            OrdenCompra.empresa_id == empresa_id,
            OrdenCompra.orden_compra_id == orden_compra_id,
        )
        .first()
    )
