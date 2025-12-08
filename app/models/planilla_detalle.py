from sqlalchemy import Column, Integer, Numeric, ForeignKey, String
from database import Base


class PlanillaDetalle(Base):
    __tablename__ = "planilla_detalle"

    detalle_id = Column(Integer, primary_key=True)
    planilla_id = Column(Integer, ForeignKey("planilla.planilla_id"), nullable=False)
    empleado_id = Column(Integer, ForeignKey("empleado.empleado_id"), nullable=False)

    salario_base = Column(Numeric(14, 2))
    horas_extra = Column(Numeric(14, 2))
    monto_horas_extra = Column(Numeric(14, 2))

    incapacidades = Column(Numeric(14, 2), default=0)
    vacaciones = Column(Numeric(14, 2), default=0)
    bonos = Column(Numeric(14, 2), default=0)

    total_devengado = Column(Numeric(14, 2))

    total_obrero = Column(Numeric(14, 2))
    total_patrono = Column(Numeric(14, 2))
    renta = Column(Numeric(14, 2))

    neto_pagar = Column(Numeric(14, 2))
