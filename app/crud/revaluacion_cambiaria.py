from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.revaluacion_cambiaria import RevaluacionCambiaria, RevaluacionCambiariaDetalle
from app.models.saldo_moneda_cuenta import SaldoMonedaCuenta
from app.schemas.revaluacion_cambiaria import RevaluacionCambiariaCrear


def _dec(valor) -> Decimal:
    if valor is None:
        return Decimal("0.00")
    return Decimal(str(valor))


def generar_revaluacion_cambiaria(
    db: Session,
    datos: RevaluacionCambiariaCrear,
    empresa_id: int,
    usuario_id: int,
):
    tc_ant = _dec(datos.tipo_cambio_anterior)
    tc_nuevo = _dec(datos.tipo_cambio_nuevo)

    saldos = (
        db.query(SaldoMonedaCuenta)
        .filter(
            SaldoMonedaCuenta.empresa_id == empresa_id,
            SaldoMonedaCuenta.moneda_id == datos.moneda_id,
        )
        .all()
    )

    if not saldos:
        raise ValueError("No hay saldos en moneda extranjera para revaluar.")

    total_ajuste = Decimal("0.00")

    rev = RevaluacionCambiaria(
        empresa_id=empresa_id,
        moneda_id=datos.moneda_id,
        fecha=datos.fecha,
        tipo_cambio_anterior=tc_ant,
        tipo_cambio_nuevo=tc_nuevo,
        total_ajuste=Decimal("0.00"),
        estado="borrador",
        comprobante_id=datos.comprobante_id,
        created_by=usuario_id,
        created_at=datetime.utcnow(),
    )
    db.add(rev)
    db.commit()
    db.refresh(rev)

    for saldo in saldos:
        saldo_moneda = _dec(saldo.saldo_moneda)
        if saldo_moneda == 0:
            continue

        valor_ant = saldo_moneda * tc_ant
        valor_nue = saldo_moneda * tc_nuevo
        ajuste = valor_nue - valor_ant

        total_ajuste += ajuste

        det = RevaluacionCambiariaDetalle(
            revaluacion_id=rev.revaluacion_id,
            cuenta_id=saldo.cuenta_id,
            saldo_moneda=saldo_moneda,
            valor_anterior=valor_ant,
            valor_nuevo=valor_nue,
            ajuste=ajuste,
        )
        db.add(det)

    rev.total_ajuste = total_ajuste
    db.commit()
    db.refresh(rev)
    return rev


def listar_revaluaciones(db: Session, empresa_id: int):
    return (
        db.query(RevaluacionCambiaria)
        .filter(RevaluacionCambiaria.empresa_id == empresa_id)
        .order_by(RevaluacionCambiaria.fecha.desc(), RevaluacionCambiaria.revaluacion_id.desc())
        .all()
    )


def obtener_revaluacion(db: Session, empresa_id: int, revaluacion_id: int):
    return (
        db.query(RevaluacionCambiaria)
        .filter(
            RevaluacionCambiaria.empresa_id == empresa_id,
            RevaluacionCambiaria.revaluacion_id == revaluacion_id,
        )
        .first()
    )
