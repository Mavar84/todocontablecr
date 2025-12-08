from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, TIMESTAMP
from database import Base


class InventarioMovimiento(Base):
    __tablename__ = "inventario_movimiento"

    movimiento_inventario_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("producto.producto_id"), nullable=False)
    bodega_id = Column(Integer, ForeignKey("bodega.bodega_id"), nullable=False)

    fecha = Column(Date, nullable=False)
    tipo = Column(String, nullable=False)  # entrada, salida
    referencia = Column(String, nullable=True)
    origen = Column(String, nullable=True)  # texto libre: factura_venta, factura_compra, ajuste, etc.
    origen_id = Column(Integer, nullable=True)

    cantidad = Column(Numeric(14, 4), nullable=False)
    costo_unitario = Column(Numeric(14, 4), nullable=False)
    costo_total = Column(Numeric(14, 4), nullable=False)

    comprobante_id = Column(Integer, ForeignKey("comprobante.comprobante_id"), nullable=True)

    created_by = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
