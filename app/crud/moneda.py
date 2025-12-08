from datetime import datetime
from sqlalchemy.orm import Session

from app.models.moneda import Moneda
from app.schemas.moneda import MonedaCrear, MonedaActualizar


def crear_moneda(db: Session, datos: MonedaCrear):
    if datos.es_base:
        db.query(Moneda).update({Moneda.es_base: False})

    moneda = Moneda(
        codigo=datos.codigo,
        nombre=datos.nombre,
        simbolo=datos.simbolo,
        es_base=datos.es_base,
        decimales=datos.decimales,
        actualizada_en=datetime.utcnow(),
    )
    db.add(moneda)
    db.commit()
    db.refresh(moneda)
    return moneda


def listar_monedas(db: Session):
    return db.query(Moneda).order_by(Moneda.codigo).all()


def obtener_moneda(db: Session, moneda_id: int):
    return (
        db.query(Moneda)
        .filter(Moneda.moneda_id == moneda_id)
        .first()
    )


def actualizar_moneda(db: Session, moneda_id: int, datos: MonedaActualizar):
    moneda = obtener_moneda(db, moneda_id)
    if not moneda:
        return None

    cambios = datos.model_dump(exclude_unset=True)

    if cambios.get("es_base") is True:
        db.query(Moneda).update({Moneda.es_base: False})

    for campo, valor in cambios.items():
        setattr(moneda, campo, valor)

    moneda.actualizada_en = datetime.utcnow()
    db.commit()
    db.refresh(moneda)
    return moneda
