from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base


class FacturaCompra(Base):
    __tablename__ = "factura_compra"

    factura_compra_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    proveedor_id = Column(Integer, ForeignKey("proveedor.proveedor_id"), nullable=False)

    orden_compra_id = Column(Integer, ForeignKey("orden_compra.orden_compra_id"), nullable=True)

    numero = Column(String, nullable=True)
    fecha = Column(Date, nullable=False)

    moneda_id = Column(Integer, ForeignKey("moneda.moneda_id"), nullable=True)

    subtotal = Column(Numeric(14, 2), nullable=True)
    descuento_total = Column(Numeric(14, 2), nullable=True)
    impuesto_total = Column(Numeric(14, 2), nullable=True)
    total = Column(Numeric(14, 2), nullable=True)

    estado = Column(String, nullable=True)  # registrada, anulada

    comprobante_id = Column(Integer, ForeignKey("comprobante.comprobante_id"), nullable=True)
    bodega_entrada_id = Column(Integer, ForeignKey("bodega.bodega_id"), nullable=True)

    detalles = relationship(
        "FacturaCompraDetalle",
        back_populates="factura",
        cascade="all, delete-orphan"
    )
