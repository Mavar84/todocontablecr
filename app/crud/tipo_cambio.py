from sqlalchemy.orm import Session
from datetime import date

from app.models.tipo_cambio import TipoCambio
from app.models.moneda import Moneda
from app.schemas.tipo_cambio import TipoCambioCrear


def crear_tipo_cambio(db: Session, datos: TipoCambioCrear):
    moneda = db.query(Moneda).filter(Moneda.moneda_id == datos.moneda_id).first()
    if not moneda:
        raise ValueError("Moneda no encontrada")

    tc = TipoCambio(
        moneda_id=datos.moneda_id,
        fecha=datos.fecha,
        compra=datos.compra,
        venta=datos.venta,
        oficial=datos.oficial,
    )
    db.add(tc)

    moneda.tasa_referencia = datos.oficial
    db.commit()
    db.refresh(tc)
    return tc


def obtener_tipo_cambio_fecha(db: Session, moneda_id: int, fecha: date):
    return (
        db.query(TipoCambio)
        .filter(
            TipoCambio.moneda_id == moneda_id,
            TipoCambio.fecha == fecha,
        )
        .first()
    )


def listar_tipos_cambio(db: Session, moneda_id: int):
    return (
        db.query(TipoCambio)
        .filter(TipoCambio.moneda_id == moneda_id)
        .order_by(TipoCambio.fecha.desc())
        .all()
    )
