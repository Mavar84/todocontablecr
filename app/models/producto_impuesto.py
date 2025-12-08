from sqlalchemy import Column, Integer, ForeignKey, Boolean, Numeric, TIMESTAMP
from database import Base


class ProductoImpuesto(Base):
    __tablename__ = "producto_impuesto"

    producto_impuesto_id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("producto.producto_id"), nullable=False)
    impuesto_id = Column(Integer, ForeignKey("impuesto.impuesto_id"), nullable=False)

    tarifa_especifica = Column(Numeric(6,3), nullable=True)  # si este producto tiene tarifa distinta a la del impuesto
    activo = Column(Boolean, default=True)

    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)
