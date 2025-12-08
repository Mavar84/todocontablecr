from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Numeric,
    ForeignKey,
    TIMESTAMP,
    UniqueConstraint,
)
from database import Base


class Presupuesto(Base):
    __tablename__ = "presupuesto"

    presupuesto_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    nombre = Column(String, nullable=False)
    anio = Column(Integer, nullable=False)
    periodo = Column(String, nullable=True)  # "ANUAL", "MENSUAL", "TRIMESTRAL" (solo descriptivo)

    estado = Column(String, nullable=False, default="borrador")  # borrador, aprobado, cerrado

    descripcion = Column(String, nullable=True)

    creado_por = Column(Integer, nullable=True)
    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_por = Column(Integer, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "empresa_id",
            "anio",
            "nombre",
            name="uq_presupuesto_empresa_anio_nombre",
        ),
    )
