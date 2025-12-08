from datetime import datetime
from sqlalchemy.orm import Session

from app.models.factura_electronica import FacturaElectronica
from app.schemas.factura_electronica import (
    FacturaElectronicaCrear,
    FacturaElectronicaActualizar,
)


def crear_factura_electronica(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    datos: FacturaElectronicaCrear,
):
    fe = FacturaElectronica(
        empresa_id=empresa_id,
        factura_id=datos.factura_id,
        tipo_documento=datos.tipo_documento,
        clave=datos.clave,
        consecutivo=datos.consecutivo,
        fecha_generacion=datos.fecha_generacion,
        fecha_envio=datos.fecha_envio,
        fecha_respuesta=datos.fecha_respuesta,
        xml_sin_firma=datos.xml_sin_firma,
        xml_firmado=datos.xml_firmado,
        xml_enviado=datos.xml_enviado,
        xml_respuesta=datos.xml_respuesta,
        estado_hacienda=datos.estado_hacienda,
        codigo_respuesta=datos.codigo_respuesta,
        mensaje_respuesta=datos.mensaje_respuesta,
        creado_por=usuario_id,
        creado_en=datetime.utcnow(),
    )
    db.add(fe)
    db.commit()
    db.refresh(fe)
    return fe


def obtener_fe_por_factura(db: Session, empresa_id: int, factura_id: int):
    return (
        db.query(FacturaElectronica)
        .filter(
            FacturaElectronica.empresa_id == empresa_id,
            FacturaElectronica.factura_id == factura_id,
        )
        .first()
    )


def obtener_fe(db: Session, empresa_id: int, fe_id: int):
    return (
        db.query(FacturaElectronica)
        .filter(
            FacturaElectronica.empresa_id == empresa_id,
            FacturaElectronica.fe_id == fe_id,
        )
        .first()
    )


def actualizar_estado_fe(
    db: Session,
    empresa_id: int,
    fe_id: int,
    usuario_id: int,
    datos: FacturaElectronicaActualizar,
):
    fe = obtener_fe(db, empresa_id, fe_id)
    if not fe:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(fe, campo, valor)

    fe.actualizado_por = usuario_id
    fe.actualizado_en = datetime.utcnow()

    db.commit()
    db.refresh(fe)
    return fe
