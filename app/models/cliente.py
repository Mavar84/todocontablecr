from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, TIMESTAMP
from database import Base


class Cliente(Base):
    __tablename__ = "cliente"

    cliente_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    nombre = Column(String, nullable=False)
    identificacion = Column(String, nullable=True)          # cédula física/jurídica/NITE
    tipo_identificacion = Column(String, nullable=True)     # FISICA, JURIDICA, DIMEX, NITE
    correo = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    direccion = Column(String, nullable=True)

    limite_credito = Column(Numeric(14, 2), nullable=True)
    dias_credito = Column(Integer, nullable=True)

    activo = Column(Boolean, default=True)

    creado_por = Column(Integer, nullable=True)
    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_por = Column(Integer, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)
