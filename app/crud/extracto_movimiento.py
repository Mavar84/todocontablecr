from datetime import datetime
from sqlalchemy.orm import Session

from app.models.extracto_movimiento import ExtractoMovimiento
from app.models.extracto_bancario import ExtractoBancario
from app.schemas.extracto_movimiento import ExtractoMovimientoCrear, ExtractoMovimientoActualizar


def crear_extracto_movimiento(
    db: Session,
    empresa_id: int,
    datos: ExtractoMovimientoCrear,
):
    ext = (
        db.query(ExtractoBancario)
        .filter(
            ExtractoBancario.extracto_id == datos.extracto_id,
            ExtractoBancario.empresa_id == empresa_id,
        )
        .first()
    )
    if not ext:
        raise ValueError("Extracto bancario no encontrado para esta empresa")

    mov = ExtractoMovimiento(
        extracto_id=datos.extracto_id,
        empresa_id=empresa_id,
        cuenta_bancaria_id=datos.cuenta_bancaria_id,
        fecha_movimiento=datos.fecha_movimiento,
        descripcion=datos.descripcion,
        referencia=datos.referencia,
        monto=datos.monto,
        tipo=datos.tipo,
        saldo_resultante=datos.saldo_resultante,
        conciliado=datos.conciliado,
        creado_en=datetime.utcnow(),
    )
    db.add(mov)
    db.commit()
    db.refresh(mov)
    return mov


def listar_extracto_movimientos(
    db: Session,
    empresa_id: int,
    extracto_id: int,
):
    return (
        db.query(ExtractoMovimiento)
        .filter(
            ExtractoMovimiento.empresa_id == empresa_id,
            ExtractoMovimiento.extracto_id == extracto_id,
        )
        .order_by(ExtractoMovimiento.fecha_movimiento, ExtractoMovimiento.extracto_movimiento_id)
        .all()
    )


def obtener_extracto_movimiento(
    db: Session,
    empresa_id: int,
    extracto_movimiento_id: int,
):
    return (
        db.query(ExtractoMovimiento)
        .filter(
            ExtractoMovimiento.empresa_id == empresa_id,
            ExtractoMovimiento.extracto_movimiento_id == extracto_movimiento_id,
        )
        .first()
    )


def actualizar_extracto_movimiento(
    db: Session,
    empresa_id: int,
    extracto_movimiento_id: int,
    datos: ExtractoMovimientoActualizar,
):
    mov = obtener_extracto_movimiento(db, empresa_id, extracto_movimiento_id)
    if not mov:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(mov, campo, valor)

    mov.actualizado_en = datetime.utcnow()
    db.commit()
    db.refresh(mov)
    return mov
