from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.factura_venta import FacturaVenta
from app.models.factura_venta_detalle import FacturaVentaDetalle
from app.schemas.factura_venta import FacturaVentaCreate
from app.schemas.cuenta_cobrar import CxCCreate
from app.crud.cuenta_cobrar import crear_cxc


def _decimal(value: float | None) -> Decimal:
    if value is None:
        return Decimal("0.00")
    return Decimal(str(value))


def crear_factura(
    db: Session,
    data: FacturaVentaCreate,
    empresa_id: int,
    usuario_id: int,
):
    if not data.detalles or len(data.detalles) == 0:
        raise ValueError("La factura debe tener al menos una línea")

    subtotal = Decimal("0.00")
    descuento_total = Decimal("0.00")
    impuesto_total = Decimal("0.00")

    for det in data.detalles:
        cantidad = _decimal(det.cantidad)
        precio = _decimal(det.precio_unitario)
        desc = _decimal(det.descuento)
        imp = _decimal(det.impuesto)

        linea_bruta = cantidad * precio
        subtotal += linea_bruta
        descuento_total += desc
        impuesto_total += imp

    total = subtotal - descuento_total + impuesto_total

    nueva = FacturaVenta(
        empresa_id=empresa_id,
        cliente_id=data.cliente_id,
        numero=data.numero,
        fecha=data.fecha,
        moneda_id=data.moneda_id,
        subtotal=subtotal,
        descuento_total=descuento_total,
        impuesto_total=impuesto_total,
        total=total,
        estado="emitida",
        comprobante_id=data.comprobante_id,
        bodega_salida_id=data.bodega_salida_id,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    for det in data.detalles:
        cantidad = _decimal(det.cantidad)
        precio = _decimal(det.precio_unitario)
        desc = _decimal(det.descuento)
        imp = _decimal(det.impuesto)
        linea_bruta = cantidad * precio
        total_linea = linea_bruta - desc + imp

        nuevo_det = FacturaVentaDetalle(
            factura_id=nueva.factura_id,
            producto_id=det.producto_id,
            descripcion=det.descripcion,
            cantidad=cantidad,
            precio_unitario=precio,
            descuento=desc,
            impuesto=imp,
            total_linea=total_linea,
            cuenta_ingreso_id=det.cuenta_ingreso_id,
        )
        db.add(nuevo_det)

    db.commit()
    db.refresh(nueva)

    if data.es_credito:
        cxc_data = CxCCreate(
            cliente_id=data.cliente_id,
            descripcion=data.descripcion_cxc or f"Factura #{nueva.numero or nueva.factura_id}",
            fecha_emision=data.fecha,
            fecha_vencimiento=data.fecha_vencimiento,
            monto_original=float(total),
            comprobante_id=data.comprobante_id,
            factura_id=nueva.factura_id,
        )
        crear_cxc(db, cxc_data, empresa_id, usuario_id)

    return nueva


def listar_facturas(db: Session, empresa_id: int):
    return (
        db.query(FacturaVenta)
        .filter(FacturaVenta.empresa_id == empresa_id)
        .order_by(FacturaVenta.fecha.desc(), FacturaVenta.factura_id.desc())
        .all()
    )


def obtener_factura(db: Session, empresa_id: int, factura_id: int):
    return (
        db.query(FacturaVenta)
        .filter(
            FacturaVenta.empresa_id == empresa_id,
            FacturaVenta.factura_id == factura_id,
        )
        .first()
    )
