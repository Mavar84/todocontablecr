from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP
from database import Base


class OrdenTrabajoMaterialPlan(Base):
    __tablename__ = "orden_trabajo_material_plan"

    material_plan_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    orden_trabajo_id = Column(Integer, ForeignKey("orden_trabajo.orden_trabajo_id"), nullable=False)

    producto_id = Column(Integer, ForeignKey("producto.producto_id"), nullable=False)
    bodega_id = Column(Integer, ForeignKey("bodega.bodega_id"), nullable=True)

    cantidad_planeada = Column(Numeric(14, 4), nullable=False)
    unidad = Column(String, nullable=True)
    costo_unitario_estimado = Column(Numeric(14, 4), nullable=True)
    costo_total_estimado = Column(Numeric(14, 2), nullable=True)

    comentario = Column(String, nullable=True)

    creado_por = Column(Integer, nullable=True)
    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_por = Column(Integer, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)
