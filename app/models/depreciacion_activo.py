from sqlalchemy import Column, Integer, Date, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base


class DepreciacionActivo(Base):
    __tablename__ = "depreciacion_activo"

    depreciacion_id = Column(Integer, primary_key=True, index=True)
    activo_id = Column(Integer, ForeignKey("activo_fijo.activo_id"), nullable=False)

    fecha = Column(Date, nullable=False)
    monto = Column(Numeric(14,2), nullable=False)

    comprobante_id = Column(Integer, ForeignKey("comprobante.comprobante_id"), nullable=True)

    created_by = Column(Integer)
    created_at = Column(TIMESTAMP)

    activo = relationship("ActivoFijo", back_populates="depreciaciones")
