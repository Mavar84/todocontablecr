from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal

from app.models.activo_fijo import ActivoFijo
from app.models.depreciacion_activo import DepreciacionActivo
from app.schemas.depreciacion_activo import DepreciacionActivoCrear


def calcular_depreciacion_mensual(activo: ActivoFijo):
    vida = Decimal(activo.vida_util_meses)
    costo = Decimal(activo.costo)
    residual = Decimal(activo.valor_residual)

    depreciable = costo - residual
    return depreciable / vida


def generar_depreciacion(
    db: Session,
    activo_id: int,
    empresa_id: int,
    fecha,
    usuario_id: int,
    comprobante_id: int | None = None,
):
    activo = (
        db.query(ActivoFijo)
        .filter(
            ActivoFijo.empresa_id == empresa_id,
            ActivoFijo.activo_id == activo_id,
        )
        .first()
    )

    if not activo:
        return None

    monto = calcular_depreciacion_mensual(activo)
    monto_f = float(monto)

    nueva = DepreciacionActivo(
        activo_id=activo.activo_id,
        fecha=fecha,
        monto=monto_f,
        comprobante_id=comprobante_id,
        created_by=usuario_id,
        created_at=datetime.utcnow(),
    )

    db.add(nueva)
    db.commit()

    # actualizar activo
    activo.depreciacion_acumulada += monto
    activo.valor_en_libros = activo.costo - activo.depreciacion_acumulada

    db.commit()
    db.refresh(nueva)
    db.refresh(activo)

    return nueva
