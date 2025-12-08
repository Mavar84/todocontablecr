from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, TIMESTAMP
from database import Base


class RetencionConfig(Base):
    __tablename__ = "retencion_config"

    retencion_config_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    tipo = Column(String, nullable=False)             # IVA, RENTA
    nombre = Column(String, nullable=False)           # Retención IVA 50%, Retención Renta Profesionales 2%, etc.

    porcentaje = Column(Numeric(6,3), nullable=False) # porcentaje de retención
    base_minima = Column(Numeric(14,2), nullable=True)  # monto mínimo para aplicar

    aplica_en_ventas = Column(Boolean, default=False)
    aplica_en_compras = Column(Boolean, default=True)

    cuenta_retencion_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=False)

    activo = Column(Boolean, default=True)

    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)
