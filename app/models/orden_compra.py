from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base


class OrdenCompra(Base):
    __tablename__ = "orden_compra"

    orden_compra_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    proveedor_id = Column(Integer, ForeignKey("proveedor.proveedor_id"), nullable=False)

    numero = Column(String, nullable=True)
    fecha = Column(Date, nullable=False)
    estado = Column(String, nullable=False, default="borrador")  # borrador, aprobada, cerrada, anulada

    moneda_id = Column(Integer, ForeignKey("moneda.moneda_id"), nullable=True)

    subtotal = Column(Numeric(14, 2), nullable=True)
    descuento_total = Column(Numeric(14, 2), nullable=True)
    impuesto_total = Column(Numeric(14, 2), nullable=True)
    total = Column(Numeric(14, 2), nullable=True)

    bodega_entrada_id = Column(Integer, ForeignKey("bodega.bodega_id"), nullable=True)

    created_by = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    detalles = relationship(
        "OrdenCompraDetalle",
        back_populates="orden",
        cascade="all, delete-orphan"
    )
