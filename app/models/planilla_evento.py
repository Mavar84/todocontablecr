from sqlalchemy import Column, Integer, Numeric, String, Date, ForeignKey, TIMESTAMP
from database import Base


class PlanillaEvento(Base):
    __tablename__ = "planilla_evento"

    evento_id = Column(Integer, primary_key=True)
    empleado_id = Column(Integer, ForeignKey("empleado.empleado_id"), nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    fecha = Column(Date, nullable=False)
    tipo = Column(String, nullable=False)  # horas_extra, incapacidad, vacaciones, permiso, bono
    cantidad = Column(Numeric(14, 2), nullable=False)
    monto = Column(Numeric(14, 2), nullable=True)
    comentario = Column(String, nullable=True)

    creado_en = Column(TIMESTAMP)
