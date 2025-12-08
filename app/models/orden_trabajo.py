from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, TIMESTAMP
from database import Base


class OrdenTrabajo(Base):
    __tablename__ = "orden_trabajo"

    orden_trabajo_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    codigo = Column(String, nullable=False, index=True)   # OT-2025-001
    descripcion = Column(String, nullable=True)

    producto_final_id = Column(Integer, ForeignKey("producto.producto_id"), nullable=False)
    cantidad_planeada = Column(Numeric(14, 4), nullable=False)
    cantidad_producida = Column(Numeric(14, 4), nullable=True, default=0)

    fecha_creacion = Column(Date, nullable=False)
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)

    estado = Column(String, nullable=False, default="planeada")
    # planeada, en_proceso, finalizada, cerrada, cancelada

    centro_costo_id = Column(Integer, ForeignKey("centro_costo.centro_costo_id"), nullable=True)
    bodega_origen_id = Column(Integer, ForeignKey("bodega.bodega_id"), nullable=True)
    bodega_destino_id = Column(Integer, ForeignKey("bodega.bodega_id"), nullable=True)

    costo_materiales = Column(Numeric(14, 2), nullable=False, default=0)
    costo_mano_obra = Column(Numeric(14, 2), nullable=False, default=0)
    costo_indirectos = Column(Numeric(14, 2), nullable=False, default=0)
    costo_total = Column(Numeric(14, 2), nullable=False, default=0)
    costo_unitario = Column(Numeric(14, 4), nullable=True)

    creado_por = Column(Integer, nullable=True)
    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_por = Column(Integer, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)
