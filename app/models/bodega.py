from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from database import Base


class Bodega(Base):
    __tablename__ = "bodega"

    bodega_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    activo = Column(Boolean, default=True)

    created_by = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
