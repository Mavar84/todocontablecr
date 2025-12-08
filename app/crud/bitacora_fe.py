from datetime import datetime
from sqlalchemy.orm import Session

from app.models.bitacora_fe import BitacoraFE
from app.schemas.bitacora_fe import BitacoraFECrear


def registrar_evento_fe(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    datos: BitacoraFECrear,
):
    b = BitacoraFE(
        empresa_id=empresa_id,
        tipo=datos.tipo,
        referencia_id=datos.referencia_id,
        accion=datos.accion,
        detalle=datos.detalle,
        estado=datos.estado,
        creado_por=usuario_id,
        creado_en=datetime.utcnow(),
    )
    db.add(b)
    db.commit()
    db.refresh(b)
    return b
