from datetime import datetime
from sqlalchemy.orm import Session

from app.models.certificado_firma import CertificadoFirma
from app.schemas.certificado_firma import CertificadoFirmaCrear, CertificadoFirmaActualizar


def crear_certificado(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    datos: CertificadoFirmaCrear,
):
    cert = CertificadoFirma(
        empresa_id=empresa_id,
        nombre=datos.nombre,
        archivo_p12_base64=datos.archivo_p12_base64,
        pin=datos.pin,
        fecha_vencimiento=datos.fecha_vencimiento,
        activo=datos.activo,
        creado_por=usuario_id,
        creado_en=datetime.utcnow(),
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert


def listar_certificados(db: Session, empresa_id: int):
    return (
        db.query(CertificadoFirma)
        .filter(CertificadoFirma.empresa_id == empresa_id)
        .order_by(CertificadoFirma.fecha_vencimiento.desc().nulls_last())
        .all()
    )


def obtener_certificado(db: Session, empresa_id: int, certificado_id: int):
    return (
        db.query(CertificadoFirma)
        .filter(
            CertificadoFirma.empresa_id == empresa_id,
            CertificadoFirma.certificado_id == certificado_id,
        )
        .first()
    )


def actualizar_certificado(
    db: Session,
    empresa_id: int,
    certificado_id: int,
    usuario_id: int,
    datos: CertificadoFirmaActualizar,
):
    cert = obtener_certificado(db, empresa_id, certificado_id)
    if not cert:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(cert, campo, valor)

    cert.actualizado_por = usuario_id
    cert.actualizado_en = datetime.utcnow()

    db.commit()
    db.refresh(cert)
    return cert
