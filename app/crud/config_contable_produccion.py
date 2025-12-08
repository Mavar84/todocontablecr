from sqlalchemy.orm import Session
from app.models.config_contable_produccion import ConfigContableProduccion
from app.schemas.config_contable_produccion import ConfigContableProduccionCrear


def guardar_config_contable_produccion(db: Session, empresa_id: int, datos: ConfigContableProduccionCrear):
    existente = db.query(ConfigContableProduccion).filter(
        ConfigContableProduccion.empresa_id == empresa_id
    ).first()

    if existente:
        for campo, valor in datos.model_dump().items():
            setattr(existente, campo, valor)
        db.commit()
        db.refresh(existente)
        return existente

    nuevo = ConfigContableProduccion(
        empresa_id=empresa_id,
        **datos.model_dump(),
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def obtener_config_contable_produccion(db: Session, empresa_id: int):
    return (
        db.query(ConfigContableProduccion)
        .filter(ConfigContableProduccion.empresa_id == empresa_id)
        .first()
    )
