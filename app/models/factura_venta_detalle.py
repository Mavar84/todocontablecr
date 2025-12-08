from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base


class FacturaVentaDetalle(Base):
    __tablename__ = "factura_venta_detalle"

    factura_detalle_id = Column(Integer, primary_key=True, index=True)
    factura_id = Column(Integer, ForeignKey("factura_venta.factura_id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("producto.producto_id"), nullable=True)

    descripcion = Column(String, nullable=True)
    cantidad = Column(Numeric(14, 2), nullable=False)
    precio_unitario = Column(Numeric(14, 2), nullable=False)
    descuento = Column(Numeric(14, 2), nullable=True)
    impuesto = Column(Numeric(14, 2), nullable=True)
    total_linea = Column(Numeric(14, 2), nullable=True)

    cuenta_ingreso_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=True)

    factura = relationship("FacturaVenta", back_populates="detalles")
