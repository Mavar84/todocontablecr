from sqlalchemy import Column, Integer, String, Boolean, Numeric, TIMESTAMP
from database import Base


class Moneda(Base):
    __tablename__ = "moneda"

    moneda_id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, nullable=False, unique=True)      # CRC, USD, EUR
    nombre = Column(String, nullable=False)                   # Colón costarricense, Dólar estadounidense
    simbolo = Column(String, nullable=True)                   # ₡, $, €

    es_base = Column(Boolean, default=False)                  # true para la moneda funcional de la empresa
    decimales = Column(Integer, default=2)

    tasa_referencia = Column(Numeric(18,6), nullable=True)    # opcional, último tipo de cambio conocido
    actualizada_en = Column(TIMESTAMP, nullable=True)
