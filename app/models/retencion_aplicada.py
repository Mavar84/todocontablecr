from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP
from database import Base


class RetencionAplicada(Base):
    __tablename__ = "retencion_aplicada"

    retencion_aplicada_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    retencion_config_id = Column(Integer, ForeignKey("retencion_config.retencion_config_id"), nullable=False)

    origen_tipo = Column(String, nullable=False)      # factura_venta, factura_compra, pago, etc.
    origen_id = Column(Integer, nullable=False)       # id del documento origen

    monto_base = Column(Numeric(14,2), nullable=False)
    monto_retencion = Column(Numeric(14,2), nullable=False)

    comprobante_id = Column(Integer, ForeignKey("comprobante.comprobante_id"), nullable=True)

    creado_en = Column(TIMESTAMP, nullable=True)
