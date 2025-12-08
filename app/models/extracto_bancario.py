from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, TIMESTAMP
from database import Base


class ExtractoBancario(Base):
    __tablename__ = "extracto_bancario"

    extracto_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    cuenta_bancaria_id = Column(Integer, ForeignKey("cuenta_bancaria.cuenta_bancaria_id"), nullable=False)

    fecha_desde = Column(Date, nullable=False)
    fecha_hasta = Column(Date, nullable=False)

    saldo_inicial = Column(Numeric(14, 2), nullable=True)
    saldo_final = Column(Numeric(14, 2), nullable=True)

    archivo_url = Column(String, nullable=True)            # URL del PDF/CSV original
    observaciones = Column(String, nullable=True)

    estado = Column(String, nullable=False, default="importado")  # importado, conciliado_parcial, conciliado_total

    creado_por = Column(Integer, nullable=True)
    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_por = Column(Integer, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)
