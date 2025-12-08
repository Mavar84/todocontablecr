from datetime import datetime
from sqlalchemy.orm import Session

from app.models.extracto_bancario import ExtractoBancario
from app.schemas.extracto_bancario import ExtractoBancarioCrear, ExtractoBancarioActualizar


def crear_extracto(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    datos: ExtractoBancarioCrear,
):
    ext = ExtractoBancario(
        empresa_id=empresa_id,
        cuenta_bancaria_id=datos.cuenta_bancaria_id,
        fecha_desde=datos.fecha_desde,
        fecha_hasta=datos.fecha_hasta,
        saldo_inicial=datos.saldo_inicial,
        saldo_final=datos.saldo_final,
        archivo_url=datos.archivo_url,
        observaciones=datos.observaciones,
        estado=datos.estado,
        creado_por=usuario_id,
        creado_en=datetime.utcnow(),
    )
    db.add(ext)
    db.commit()
    db.refresh(ext)
    return ext


def listar_extractos(
    db: Session,
    empresa_id: int,
    cuenta_bancaria_id: int | None = None,
):
    q = db.query(ExtractoBancario).filter(ExtractoBancario.empresa_id == empresa_id)
    if cuenta_bancaria_id:
        q = q.filter(ExtractoBancario.cuenta_bancaria_id == cuenta_bancaria_id)
    return q.order_by(ExtractoBancario.fecha_desde.desc()).all()


def obtener_extracto(
    db: Session,
    empresa_id: int,
    extracto_id: int,
):
    return (
        db.query(ExtractoBancario)
        .filter(
            ExtractoBancario.empresa_id == empresa_id,
            ExtractoBancario.extracto_id == extracto_id,
        )
        .first()
    )


def actualizar_extracto(
    db: Session,
    empresa_id: int,
    extracto_id: int,
    usuario_id: int,
    datos: ExtractoBancarioActualizar,
):
    ext = obtener_extracto(db, empresa_id, extracto_id)
    if not ext:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(ext, campo, valor)

    ext.actualizado_por = usuario_id
    ext.actualizado_en = datetime.utcnow()

    db.commit()
    db.refresh(ext)
    return ext
