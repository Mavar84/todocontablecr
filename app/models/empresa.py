from sqlalchemy import Column, Integer, String, TIMESTAMP
from database import Base

class Empresa(Base):
    __tablename__ = "empresa"

    empresa_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    cedula_juridica = Column(String, nullable=True)
    moneda_base_id = Column(Integer, nullable=True)

    created_by = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
