from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime
)
from database import Base


class CatalogoCuenta(Base):
    __tablename__ = "catalogo_cuenta"

    cuenta_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    codigo = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    naturaleza = Column(String, nullable=True)  # activo, pasivo, ingreso, egreso, patrimonio
    tipo_saldo = Column(String, nullable=True)
    nivel = Column(Integer, nullable=True)
    es_imputable = Column(Boolean, default=True)

    cuenta_padre_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=True)

    es_depreciable = Column(Boolean, default=False)
    es_inventario = Column(Boolean, default=False)
    es_costo = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)

    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True)
