from sqlalchemy import Column, Integer, Date, Numeric, ForeignKey, TIMESTAMP
from database import Base


class EmpleadoSalarioHist(Base):
    __tablename__ = "empleado_salario_hist"

    hist_id = Column(Integer, primary_key=True)
    empleado_id = Column(Integer, ForeignKey("empleado.empleado_id"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)

    salario_base = Column(Numeric(14, 2), nullable=False)
    creado_en = Column(TIMESTAMP)
