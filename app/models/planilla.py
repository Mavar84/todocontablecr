from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, TIMESTAMP
from database import Base


class Planilla(Base):
    __tablename__ = "planilla"

    planilla_id = Column(Integer, primary_key=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    periodo = Column(String, nullable=False)        # 2025-02-Quincena1, 2025-03-Mensual
    fecha_pago = Column(Date, nullable=False)
    estado = Column(String, default="borrador")     # borrador, cerrada, contabilizada

    total_salarios = Column(Numeric(14, 2), default=0)
    total_obrero = Column(Numeric(14, 2), default=0)
    total_patrono = Column(Numeric(14, 2), default=0)
    total_renta = Column(Numeric(14, 2), default=0)
    total_neto = Column(Numeric(14, 2), default=0)

    creado_en = Column(TIMESTAMP)
    actualizado_en = Column(TIMESTAMP)
