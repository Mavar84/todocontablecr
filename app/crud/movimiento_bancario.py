from datetime import datetime
from sqlalchemy.orm import Session
from app.models.movimiento_bancario import MovimientoBancario
from app.schemas.movimiento_bancario import MovimientoBancarioCrear


def crear_movimiento_bancario(db: Session, datos: MovimientoBancarioCrear, empresa_id: int, usuario_id: int):
    mov = MovimientoBancario(
        empresa_id=empresa_id,
        cuenta_bancaria_id=datos.cuenta_bancaria_id,
        fecha=datos.fecha,
        descripcion=datos.descripcion,
        monto=datos.monto,
        comprobante_id=datos.comprobante_id,
        created_by=usuario_id,
        created_at=datetime.utcnow(),
    )
    db.add(mov)
    db.commit()
    db.refresh(mov)
    return mov


def listar_movimientos_bancarios(
    db: Session,
    empresa_id: int,
    cuenta_bancaria_id: int,
    fecha_desde=None,
    fecha_hasta=None,
):
    consulta = db.query(MovimientoBancario).filter(
        MovimientoBancario.empresa_id == empresa_id,
        MovimientoBancario.cuenta_bancaria_id == cuenta_bancaria_id,
    )
    if fecha_desde:
        consulta = consulta.filter(MovimientoBancario.fecha >= fecha_desde)
    if fecha_hasta:
        consulta = consulta.filter(MovimientoBancario.fecha <= fecha_hasta)

    return consulta.order_by(MovimientoBancario.fecha, MovimientoBancario.movimiento_bancario_id).all()


def obtener_movimiento_bancario(db: Session, empresa_id: int, movimiento_id: int):
    return (
        db.query(MovimientoBancario)
        .filter(
            MovimientoBancario.empresa_id == empresa_id,
            MovimientoBancario.movimiento_bancario_id == movimiento_id,
        )
        .first()
    )
