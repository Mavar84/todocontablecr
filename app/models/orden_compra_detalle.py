from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base


class OrdenCompraDetalle(Base):
    __tablename__ = "orden_compra_detalle"

    orden_compra_detalle_id = Column(Integer, primary_key=True, index=True)
    orden_compra_id = Column(Integer, ForeignKey("orden_compra.orden_compra_id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("producto.producto_id"), nullable=True)

    descripcion = Column(String, nullable=True)
    cantidad = Column(Numeric(14, 2), nullable=False)
    costo_unitario = Column(Numeric(14, 2), nullable=False)
    descuento = Column(Numeric(14, 2), nullable=True)
    impuesto = Column(Numeric(14, 2), nullable=True)
    total_linea = Column(Numeric(14, 2), nullable=True)

    cuenta_gasto_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=True)

    orden = relationship("OrdenCompra", back_populates="detalles")
