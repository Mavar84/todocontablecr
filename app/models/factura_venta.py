from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base


class FacturaVenta(Base):
    __tablename__ = "factura_venta"

    factura_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("cliente.cliente_id"), nullable=False)

    numero = Column(String, nullable=True)
    fecha = Column(Date, nullable=False)

    moneda_id = Column(Integer, ForeignKey("moneda.moneda_id"), nullable=True)

    subtotal = Column(Numeric(14, 2), nullable=True)
    descuento_total = Column(Numeric(14, 2), nullable=True)
    impuesto_total = Column(Numeric(14, 2), nullable=True)
    total = Column(Numeric(14, 2), nullable=True)

    estado = Column(String, nullable=True)  # borrador, emitida, anulada

    comprobante_id = Column(Integer, ForeignKey("comprobante.comprobante_id"), nullable=True)
    bodega_salida_id = Column(Integer, ForeignKey("bodega.bodega_id"), nullable=True)

    detalles = relationship(
        "FacturaVentaDetalle",
        back_populates="factura",
        cascade="all, delete-orphan"
    )
