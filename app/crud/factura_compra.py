from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.factura_compra import FacturaCompra
from app.models.factura_compra_detalle import FacturaCompraDetalle
from app.schemas.factura_compra import FacturaCompraCreate
from app.schemas.cuenta_pagar import CxPCreate
from app.crud.cuenta_pagar import crear_cxp


def _dec(value: float | None) -> Decimal:
    if value is None:
        return Decimal("0.00")
    return Decimal(str(value))


def crear_factura_compra(
    db: Session,
    data: FacturaCompraCreate,
    empresa_id: int,
    usuario_id: int,
):
    if not data.detalles or len(data.detalles) == 0:
        raise ValueError("La factura de compra debe tener al menos una línea")

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

    nueva = FacturaCompra(
        empresa_id=empresa_id,
        proveedor_id=data.proveedor_id,
        orden_compra_id=data.orden_compra_id,
        numero=data.numero,
        fecha=data.fecha,
        moneda_id=data.moneda_id,
        subtotal=subtotal,
        descuento_total=descuento_total,
        impuesto_total=impuesto_total,
        total=total,
        estado="registrada",
        comprobante_id=data.comprobante_id,
        bodega_entrada_id=data.bodega_entrada_id,
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

        nuevo_det = FacturaCompraDetalle(
            factura_compra_id=nueva.factura_compra_id,
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

    if data.es_credito:
        cxp_data = CxPCreate(
            proveedor_id=data.proveedor_id,
            descripcion=data.descripcion_cxp or f"Factura compra #{nueva.numero or nueva.factura_compra_id}",
            fecha_emision=data.fecha,
            fecha_vencimiento=data.fecha_vencimiento,
            monto_original=float(total),
            comprobante_id=data.comprobante_id,
            orden_compra_id=data.orden_compra_id,
        )
        crear_cxp(db, cxp_data, empresa_id, usuario_id)

    return nueva


def listar_facturas_compra(db: Session, empresa_id: int):
    return (
        db.query(FacturaCompra)
        .filter(FacturaCompra.empresa_id == empresa_id)
        .order_by(FacturaCompra.fecha.desc(), FacturaCompra.factura_compra_id.desc())
        .all()
    )


def obtener_factura_compra(db: Session, empresa_id: int, factura_compra_id: int):
    return (
        db.query(FacturaCompra)
        .filter(
            FacturaCompra.empresa_id == empresa_id,
            FacturaCompra.factura_compra_id == factura_compra_id,
        )
        .first()
    )
