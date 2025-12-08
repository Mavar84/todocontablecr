from sqlalchemy import Column, Integer, String, Boolean, Date, Numeric, ForeignKey, TIMESTAMP
from database import Base


class Empleado(Base):
    __tablename__ = "empleado"

    empleado_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    cedula = Column(String, nullable=False, unique=True)
    nombre = Column(String, nullable=False)
    apellido1 = Column(String, nullable=False)
    apellido2 = Column(String, nullable=True)

    fecha_ingreso = Column(Date, nullable=False)
    fecha_salida = Column(Date, nullable=True)

    tipo_contrato = Column(String, nullable=False)  # indefinido, temporal
    puesto = Column(String, nullable=True)
    departamento = Column(String, nullable=True)

    salario_base = Column(Numeric(14, 2), nullable=False)
    tipo_jornada = Column(String, nullable=False)  # mensual, quincenal, semanal

    centro_costo_id = Column(Integer, ForeignKey("centro_costo.centro_costo_id"), nullable=True)

    activo = Column(Boolean, default=True)

    creado_en = Column(TIMESTAMP)
    actualizado_en = Column(TIMESTAMP)
