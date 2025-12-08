from datetime import datetime
from sqlalchemy.orm import Session

from app.models.comprobante import Comprobante
from app.models.movimiento import Movimiento
from app.schemas.comprobante import ComprobanteCreate


def crear_comprobante(db: Session, data: ComprobanteCreate, empresa_id: int, usuario_id: int):

    total_debe = sum(item.debe for item in data.movimientos)
    total_haber = sum(item.haber for item in data.movimientos)

    if round(total_debe, 2) != round(total_haber, 2):
        raise ValueError("Los movimientos no cumplen la partida doble: debe == haber")

    nuevo = Comprobante(
        empresa_id=empresa_id,
        fecha=data.fecha,
        descripcion=data.descripcion,
        tipo_comprobante_id=data.tipo_comprobante_id,
        moneda_id=data.moneda_id,
        tipo_cambio_usado=data.tipo_cambio_usado,
        creado_por=usuario_id,
        fecha_creacion=datetime.utcnow()
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    # Agregar movimientos
    for m in data.movimientos:
        mov = Movimiento(
            comprobante_id=nuevo.comprobante_id,
            cuenta_id=m.cuenta_id,
            descripcion=m.descripcion,
            debe=m.debe,
            haber=m.haber,
            centro_costo_id=m.centro_costo_id,
            bodega_id=m.bodega_id,
            created_by=usuario_id,
            created_at=datetime.utcnow()
        )
        db.add(mov)

    db.commit()
    db.refresh(nuevo)

    return nuevo


def listar_comprobantes(db: Session, empresa_id: int):
    return (
        db.query(Comprobante)
        .filter(Comprobante.empresa_id == empresa_id)
        .order_by(Comprobante.fecha.desc())
        .all()
    )


def obtener_comprobante(db: Session, empresa_id: int, comprobante_id: int):
    return (
        db.query(Comprobante)
        .filter(
            Comprobante.empresa_id == empresa_id,
            Comprobante.comprobante_id == comprobante_id
        )
        .first()
    )
def crear_comprobante_automatico(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    fecha,
    descripcion: str,
    lineas: list,
    tipo: str,
    referencia_id: int,
):

    comprob = Comprobante(
        empresa_id=empresa_id,
        fecha=fecha,
        descripcion=descripcion,
        tipo=tipo,               # "OT"
        referencia_id=referencia_id,
        creado_por=usuario_id,
        creado_en=datetime.utcnow(),
    )

    db.add(comprob)
    db.commit()
    db.refresh(comprob)

    for l in lineas:
        mov = MovimientoContable(
            empresa_id=empresa_id,
            comprobante_id=comprob.comprobante_id,
            cuenta_id=l["cuenta_id"],
            debe=l["debe"],
            haber=l["haber"],
            detalle=l["detalle"],
            creado_por=usuario_id,
            creado_en=datetime.utcnow(),
        )
        db.add(mov)

    db.commit()
    return comprob