from datetime import datetime, date
from sqlalchemy.orm import Session

from app.models.cuenta_cobrar import CuentaCobrar, CuentaCobrarMovimiento
from app.schemas.cuenta_cobrar import CxCCreate, CxCMovCreate, CxCUpdate


def crear_cxc(db: Session, data: CxCCreate, empresa_id: int, usuario_id: int):
    nuevo = CuentaCobrar(
        empresa_id=empresa_id,
        cliente_id=data.cliente_id,
        descripcion=data.descripcion,
        fecha_emision=data.fecha_emision,
        fecha_vencimiento=data.fecha_vencimiento,
        monto_original=data.monto_original,
        saldo_actual=data.monto_original,
        estado="pendiente",
        comprobante_id=data.comprobante_id,
        factura_id=data.factura_id,
        created_by=usuario_id,
        created_at=datetime.utcnow()
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_cxc(db: Session, empresa_id: int):
    return (
        db.query(CuentaCobrar)
        .filter(CuentaCobrar.empresa_id == empresa_id)
        .order_by(CuentaCobrar.fecha_emision.desc())
        .all()
    )


def obtener_cxc(db: Session, empresa_id: int, cxc_id: int):
    return (
        db.query(CuentaCobrar)
        .filter(
            CuentaCobrar.empresa_id == empresa_id,
            CuentaCobrar.cxc_id == cxc_id
        )
        .first()
    )


def actualizar_estado(cxc: CuentaCobrar):
    if cxc.saldo_actual <= 0:
        cxc.estado = "cancelada"
    elif cxc.saldo_actual < cxc.monto_original:
        cxc.estado = "parcial"
    else:
        cxc.estado = "pendiente"

    # Vencimiento
    if cxc.fecha_vencimiento and cxc.saldo_actual > 0:
        if cxc.fecha_vencimiento < date.today():
            cxc.estado = "vencida"

    return cxc.estado


def agregar_movimiento(db: Session, cxc_id: int, data: CxCMovCreate, usuario_id: int, empresa_id: int):

    cxc = obtener_cxc(db, empresa_id, cxc_id)
    if not cxc:
        return None

    if data.tipo in ("pago", "nota_credito") and data.monto > cxc.saldo_actual:
        raise ValueError("El monto excede el saldo actual")

    mov = CuentaCobrarMovimiento(
        cxc_id=cxc_id,
        fecha=data.fecha,
        tipo=data.tipo,
        monto=data.monto,
        descripcion=data.descripcion,
        comprobante_id=data.comprobante_id,
        created_by=usuario_id,
        created_at=datetime.utcnow()
    )

    db.add(mov)

    # Actualizar saldo
    if data.tipo in ("pago", "nota_credito"):
        cxc.saldo_actual -= data.monto
    elif data.tipo == "ajuste":
        cxc.saldo_actual += data.monto
    elif data.tipo == "reversion":
        cxc.saldo_actual += data.monto

    actualizar_estado(cxc)

    db.commit()
    db.refresh(mov)
    db.refresh(cxc)

    return mov


def actualizar_cxc(db: Session, empresa_id: int, cxc_id: int, data: CxCUpdate, usuario_id: int):
    cxc = obtener_cxc(db, empresa_id, cxc_id)
    if not cxc:
        return None

    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(cxc, campo, valor)

    cxc.updated_by = usuario_id
    cxc.updated_at = datetime.utcnow()

    actualizar_estado(cxc)

    db.commit()
    db.refresh(cxc)
    return cxc
