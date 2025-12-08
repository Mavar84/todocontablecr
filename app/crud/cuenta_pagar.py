from datetime import datetime, date
from sqlalchemy.orm import Session
from app.models.cuenta_pagar import CuentaPagar, CuentaPagarMovimiento
from app.schemas.cuenta_pagar import CxPCreate, CxPMovCreate, CxPUpdate


def crear_cxp(db: Session, data: CxPCreate, empresa_id: int, usuario_id: int):
    nuevo = CuentaPagar(
        empresa_id=empresa_id,
        proveedor_id=data.proveedor_id,
        descripcion=data.descripcion,
        fecha_emision=data.fecha_emision,
        fecha_vencimiento=data.fecha_vencimiento,
        monto_original=data.monto_original,
        saldo_actual=data.monto_original,
        estado="pendiente",
        comprobante_id=data.comprobante_id,
        orden_compra_id=data.orden_compra_id,
        created_by=usuario_id,
        created_at=datetime.utcnow(),
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_cxp(db: Session, empresa_id: int):
    return (
        db.query(CuentaPagar)
        .filter(CuentaPagar.empresa_id == empresa_id)
        .order_by(CuentaPagar.fecha_emision.desc())
        .all()
    )


def obtener_cxp(db: Session, empresa_id: int, cxp_id: int):
    return (
        db.query(CuentaPagar)
        .filter(
            CuentaPagar.empresa_id == empresa_id,
            CuentaPagar.cxp_id == cxp_id,
        )
        .first()
    )


def actualizar_estado(cxp: CuentaPagar):
    if cxp.saldo_actual <= 0:
        cxp.estado = "cancelada"
    elif cxp.saldo_actual < cxp.monto_original:
        cxp.estado = "parcial"
    else:
        cxp.estado = "pendiente"

    # vencimiento
    if cxp.fecha_vencimiento and cxp.saldo_actual > 0:
        if cxp.fecha_vencimiento < date.today():
            cxp.estado = "vencida"

    return cxp.estado


def agregar_movimiento(db: Session, cxp_id: int, data: CxPMovCreate, usuario_id: int, empresa_id: int):

    cxp = obtener_cxp(db, empresa_id, cxp_id)
    if not cxp:
        return None

    # Validación de sobrepago
    if data.tipo == "pago" and data.monto > cxp.saldo_actual:
        raise ValueError("El pago excede el saldo actual")

    mov = CuentaPagarMovimiento(
        cxp_id=cxp_id,
        fecha=data.fecha,
        tipo=data.tipo,
        monto=data.monto,
        descripcion=data.descripcion,
        comprobante_id=data.comprobante_id,
        created_by=usuario_id,
        created_at=datetime.utcnow(),
    )

    db.add(mov)

    # Actualizar saldo
    if data.tipo in ("pago", "nota_credito"):
        cxp.saldo_actual -= data.monto
    elif data.tipo in ("nota_debito", "ajuste"):
        cxp.saldo_actual += data.monto
    elif data.tipo == "reversion":
        cxp.saldo_actual += data.monto

    actualizar_estado(cxp)

    db.commit()
    db.refresh(mov)
    db.refresh(cxp)

    return mov


def actualizar_cxp(db: Session, empresa_id: int, cxp_id: int, data: CxPUpdate, usuario_id: int):
    cxp = obtener_cxp(db, empresa_id, cxp_id)
    if not cxp:
        return None

    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(cxp, campo, valor)

    cxp.updated_by = usuario_id
    cxp.updated_at = datetime.utcnow()

    actualizar_estado(cxp)

    db.commit()
    db.refresh(cxp)
    return cxp
