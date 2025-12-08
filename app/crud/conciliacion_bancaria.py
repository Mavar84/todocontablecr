from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.conciliacion_bancaria import ConciliacionBancaria, ConciliacionBancariaDetalle
from app.models.cuenta_bancaria import CuentaBancaria
from app.models.movimiento_bancario import MovimientoBancario
from app.schemas.conciliacion_bancaria import ConciliacionCrear


def _dec(valor: float | None) -> Decimal:
    if valor is None:
        return Decimal("0.00")
    return Decimal(str(valor))


def _calcular_saldo_libros(
    db: Session,
    empresa_id: int,
    cuenta_bancaria_id: int,
    fecha_hasta,
):
    cuenta = (
        db.query(CuentaBancaria)
        .filter(
            CuentaBancaria.empresa_id == empresa_id,
            CuentaBancaria.cuenta_bancaria_id == cuenta_bancaria_id,
        )
        .first()
    )
    if not cuenta:
        raise ValueError("Cuenta bancaria no encontrada")

    saldo = _dec(cuenta.saldo_inicial)

    movimientos = (
        db.query(MovimientoBancario)
        .filter(
            MovimientoBancario.empresa_id == empresa_id,
            MovimientoBancario.cuenta_bancaria_id == cuenta_bancaria_id,
            MovimientoBancario.fecha <= fecha_hasta,
        )
        .all()
    )

    for mov in movimientos:
        saldo += _dec(mov.monto)

    return saldo


def crear_conciliacion(
    db: Session,
    datos: ConciliacionCrear,
    empresa_id: int,
    usuario_id: int,
):
    saldo_libros = _calcular_saldo_libros(
        db=db,
        empresa_id=empresa_id,
        cuenta_bancaria_id=datos.cuenta_bancaria_id,
        fecha_hasta=datos.fecha_hasta,
    )

    saldo_extracto = _dec(datos.saldo_extracto)
    diferencia = saldo_libros - saldo_extracto

    conc = ConciliacionBancaria(
        empresa_id=empresa_id,
        cuenta_bancaria_id=datos.cuenta_bancaria_id,
        fecha_desde=datos.fecha_desde,
        fecha_hasta=datos.fecha_hasta,
        saldo_libros=saldo_libros,
        saldo_extracto=saldo_extracto,
        diferencia=diferencia,
        estado="borrador",
        created_by=usuario_id,
        created_at=datetime.utcnow(),
    )
    db.add(conc)
    db.commit()
    db.refresh(conc)

    for det_in in datos.movimientos:
        mov = obtener_movimiento_en_cuenta(
            db=db,
            empresa_id=empresa_id,
            cuenta_bancaria_id=datos.cuenta_bancaria_id,
            movimiento_id=det_in.movimiento_bancario_id,
        )
        if not mov:
            continue

        det = ConciliacionBancariaDetalle(
            conciliacion_id=conc.conciliacion_id,
            movimiento_bancario_id=mov.movimiento_bancario_id,
            tipo_diferencia=det_in.tipo_diferencia,
            nota=det_in.nota,
        )
        db.add(det)
        mov.conciliado = True

    db.commit()
    db.refresh(conc)
    return conc


def obtener_movimiento_en_cuenta(
    db: Session,
    empresa_id: int,
    cuenta_bancaria_id: int,
    movimiento_id: int,
):
    return (
        db.query(MovimientoBancario)
        .filter(
            MovimientoBancario.empresa_id == empresa_id,
            MovimientoBancario.cuenta_bancaria_id == cuenta_bancaria_id,
            MovimientoBancario.movimiento_bancario_id == movimiento_id,
        )
        .first()
    )


def listar_conciliaciones(db: Session, empresa_id: int, cuenta_bancaria_id: int | None = None):
    q = db.query(ConciliacionBancaria).filter(ConciliacionBancaria.empresa_id == empresa_id)
    if cuenta_bancaria_id is not None:
        q = q.filter(ConciliacionBancaria.cuenta_bancaria_id == cuenta_bancaria_id)
    return q.order_by(ConciliacionBancaria.fecha_hasta.desc()).all()


def obtener_conciliacion(db: Session, empresa_id: int, conciliacion_id: int):
    return (
        db.query(ConciliacionBancaria)
        .filter(
            ConciliacionBancaria.empresa_id == empresa_id,
            ConciliacionBancaria.conciliacion_id == conciliacion_id,
        )
        .first()
    )
