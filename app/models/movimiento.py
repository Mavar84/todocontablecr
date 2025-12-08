from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base


class Movimiento(Base):
    __tablename__ = "movimiento"

    movimiento_id = Column(Integer, primary_key=True, index=True)
    comprobante_id = Column(Integer, ForeignKey("comprobante.comprobante_id"), nullable=False)

    cuenta_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=False)

    descripcion = Column(String, nullable=True)
    debe = Column(Numeric(14,2), default=0)
    haber = Column(Numeric(14,2), default=0)

    centro_costo_id = Column(Integer, ForeignKey("centro_costo.centro_costo_id"), nullable=True)
    bodega_id = Column(Integer, ForeignKey("bodega.bodega_id"), nullable=True)

    created_by = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_by = Column(Integer)
    updated_at = Column(TIMESTAMP)

    comprobante = relationship("Comprobante", back_populates="movimientos")
