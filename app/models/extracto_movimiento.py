from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Boolean, TIMESTAMP
from database import Base


class ExtractoMovimiento(Base):
    __tablename__ = "extracto_movimiento"

    extracto_movimiento_id = Column(Integer, primary_key=True, index=True)
    extracto_id = Column(Integer, ForeignKey("extracto_bancario.extracto_id"), nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    cuenta_bancaria_id = Column(Integer, ForeignKey("cuenta_bancaria.cuenta_bancaria_id"), nullable=False)

    fecha_movimiento = Column(Date, nullable=False)
    descripcion = Column(String, nullable=True)
    referencia = Column(String, nullable=True)

    monto = Column(Numeric(14, 2), nullable=False)
    tipo = Column(String, nullable=False)                  # DEBITO, CREDITO

    saldo_resultante = Column(Numeric(14, 2), nullable=True)

    conciliado = Column(Boolean, default=False)

    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)
