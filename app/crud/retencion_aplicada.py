from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.retencion_aplicada import RetencionAplicada
from app.models.retencion_config import RetencionConfig
from app.schemas.retencion_aplicada import RetencionAplicadaCrear


def aplicar_retencion(
    db: Session,
    empresa_id: int,
    datos: RetencionAplicadaCrear,
):
    config = (
        db.query(RetencionConfig)
        .filter(
            RetencionConfig.empresa_id == empresa_id,
            RetencionConfig.retencion_config_id == datos.retencion_config_id,
            RetencionConfig.activo == True,
        )
        .first()
    )
    if not config:
        raise ValueError("Configuración de retención no encontrada o inactiva")

    base = Decimal(str(datos.monto_base))
    monto_ret = Decimal(str(datos.monto_retencion))

    if config.base_minima is not None and base < config.base_minima:
        raise ValueError("El monto no alcanza la base mínima para aplicar esta retención")

    if monto_ret <= 0:
        porcentaje_calc = (config.porcentaje / Decimal("100.000")) if config.porcentaje else Decimal("0")
        monto_ret = base * porcentaje_calc

    ra = RetencionAplicada(
        empresa_id=empresa_id,
        retencion_config_id=datos.retencion_config_id,
        origen_tipo=datos.origen_tipo,
        origen_id=datos.origen_id,
        monto_base=base,
        monto_retencion=monto_ret,
        comprobante_id=datos.comprobante_id,
        creado_en=datetime.utcnow(),
    )
    db.add(ra)
    db.commit()
    db.refresh(ra)
    return ra
