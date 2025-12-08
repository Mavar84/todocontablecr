from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, TIMESTAMP
from database import Base


class OrdenTrabajoConsumoMaterial(Base):
    __tablename__ = "orden_trabajo_consumo_material"

    consumo_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    orden_trabajo_id = Column(Integer, ForeignKey("orden_trabajo.orden_trabajo_id"), nullable=False)

    producto_id = Column(Integer, ForeignKey("producto.producto_id"), nullable=False)
    bodega_id = Column(Integer, ForeignKey("bodega.bodega_id"), nullable=True)

    fecha_consumo = Column(Date, nullable=False)
    cantidad = Column(Numeric(14, 4), nullable=False)
    costo_unitario = Column(Numeric(14, 4), nullable=False)
    costo_total = Column(Numeric(14, 2), nullable=False)

    movimiento_inventario_id = Column(Integer, ForeignKey("movimiento_inventario.movimiento_inventario_id"), nullable=True)

    comentario = Column(String, nullable=True)

    creado_por = Column(Integer, nullable=True)
    creado_en = Column(TIMESTAMP, nullable=True)
