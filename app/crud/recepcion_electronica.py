from datetime import datetime
from sqlalchemy.orm import Session

from app.models.recepcion_electronica import RecepcionElectronica
from app.schemas.recepcion_electronica import (
    RecepcionElectronicaCrear,
    RecepcionElectronicaActualizar,
)


def crear_recepcion_electronica(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    datos: RecepcionElectronicaCrear,
):
    rec = RecepcionElectronica(
        empresa_id=empresa_id,
        factura_compra_id=datos.factura_compra_id,
        clave=datos.clave,
        consecutivo_emisor=datos.consecutivo_emisor,
        cedula_emisor=datos.cedula_emisor,
        fecha_recepcion=datos.fecha_recepcion,
        fecha_respuesta=datos.fecha_respuesta,
        xml_original=datos.xml_original,
        xml_aceptacion=datos.xml_aceptacion,
        estado_respuesta=datos.estado_respuesta,
        mensaje_respuesta=datos.mensaje_respuesta,
        creado_por=usuario_id,
        creado_en=datetime.utcnow(),
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


def obtener_recepcion(db: Session, empresa_id: int, recepcion_id: int):
    return (
        db.query(RecepcionElectronica)
        .filter(
            RecepcionElectronica.empresa_id == empresa_id,
            RecepcionElectronica.recepcion_id == recepcion_id,
        )
        .first()
    )


def actualizar_recepcion(
    db: Session,
    empresa_id: int,
    recepcion_id: int,
    usuario_id: int,
    datos: RecepcionElectronicaActualizar,
):
    rec = obtener_recepcion(db, empresa_id, recepcion_id)
    if not rec:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(rec, campo, valor)

    rec.actualizado_por = usuario_id
    rec.actualizado_en = datetime.utcnow()

    db.commit()
    db.refresh(rec)
    return rec
