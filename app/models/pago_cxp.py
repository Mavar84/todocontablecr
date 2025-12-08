from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, TIMESTAMP
from database import Base


class PagoCXP(Base):
    __tablename__ = "pago_cxp"

    pago_cxp_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    cxp_id = Column(Integer, ForeignKey("cuenta_pagar.cxp_id"), nullable=False)
    fecha_pago = Column(Date, nullable=False)
    moneda_id = Column(Integer, ForeignKey("moneda.moneda_id"), nullable=True)
    monto = Column(Numeric(14, 2), nullable=False)

    tipo_pago = Column(String, nullable=True)
    referencia = Column(String, nullable=True)

    comprobante_id = Column(Integer, ForeignKey("comprobante.comprobante_id"), nullable=True)

    creado_por = Column(Integer, nullable=True)
    creado_en = Column(TIMESTAMP, nullable=True)
