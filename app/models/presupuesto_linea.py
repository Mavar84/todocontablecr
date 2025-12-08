from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
    String,
    TIMESTAMP,
    UniqueConstraint,
)
from database import Base


class PresupuestoLinea(Base):
    __tablename__ = "presupuesto_linea"

    linea_id = Column(Integer, primary_key=True, index=True)
    presupuesto_id = Column(Integer, ForeignKey("presupuesto.presupuesto_id"), nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    cuenta_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=False)
    centro_costo_id = Column(Integer, ForeignKey("centro_costo.centro_costo_id"), nullable=True)

    mes = Column(Integer, nullable=True)  # 1-12; si es null se asume anual
    monto_presupuestado = Column(Numeric(14, 2), nullable=False, default=0)

    comentario = Column(String, nullable=True)

    creado_por = Column(Integer, nullable=True)
    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_por = Column(Integer, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "presupuesto_id",
            "cuenta_id",
            "centro_costo_id",
            "mes",
            name="uq_presupuesto_linea_unica",
        ),
    )
