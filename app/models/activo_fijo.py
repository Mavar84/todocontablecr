from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base


class ActivoFijo(Base):
    __tablename__ = "activo_fijo"

    activo_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    tipo_activo_id = Column(Integer, ForeignKey("tipo_activo.tipo_activo_id"), nullable=False)

    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)

    fecha_compra = Column(Date, nullable=False)
    costo = Column(Numeric(14,2), nullable=False)

    valor_residual = Column(Numeric(14,2), nullable=True)
    vida_util_meses = Column(Integer, nullable=False)

    depreciacion_acumulada = Column(Numeric(14,2), default=0)
    valor_en_libros = Column(Numeric(14,2), nullable=False)

    estado = Column(String, default="activo")  # activo, vendido, dado_de_baja

    comprobante_id = Column(Integer, ForeignKey("comprobante.comprobante_id"), nullable=True)

    created_by = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_by = Column(Integer)
    updated_at = Column(TIMESTAMP)

    depreciaciones = relationship(
        "DepreciacionActivo",
        back_populates="activo",
        cascade="all, delete-orphan"
    )
