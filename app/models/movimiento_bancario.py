from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Boolean, TIMESTAMP
from database import Base


class MovimientoBancario(Base):
    __tablename__ = "movimiento_bancario"

    movimiento_bancario_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    cuenta_bancaria_id = Column(Integer, ForeignKey("cuenta_bancaria.cuenta_bancaria_id"), nullable=False)

    fecha = Column(Date, nullable=False)
    descripcion = Column(String, nullable=True)

    monto = Column(Numeric(14, 2), nullable=False)  # positivo = depósito, negativo = retiro

    conciliado = Column(Boolean, default=False)
    comprobante_id = Column(Integer, ForeignKey("comprobante.comprobante_id"), nullable=True)

    created_by = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
