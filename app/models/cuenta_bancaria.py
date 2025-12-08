from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, TIMESTAMP
from database import Base


class CuentaBancaria(Base):
    __tablename__ = "cuenta_bancaria"

    cuenta_bancaria_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    banco_nombre = Column(String, nullable=False)
    numero_cuenta = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)

    moneda_id = Column(Integer, ForeignKey("moneda.moneda_id"), nullable=True)
    saldo_inicial = Column(Numeric(14, 2), default=0)

    activa = Column(Boolean, default=True)

    created_by = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
