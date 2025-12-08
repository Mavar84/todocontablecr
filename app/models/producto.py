from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, TIMESTAMP
from database import Base


class Producto(Base):
    __tablename__ = "producto"

    producto_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    codigo = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)

    unidad_medida = Column(String, nullable=True)
    cabys = Column(String, nullable=True)

    es_inventariable = Column(Boolean, default=True)
    activo = Column(Boolean, default=True)

    cuenta_inventario_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=True)
    cuenta_costo_venta_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=True)
    cuenta_ingreso_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=True)

    created_by = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
