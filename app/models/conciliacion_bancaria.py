from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base


class ConciliacionBancaria(Base):
    __tablename__ = "conciliacion_bancaria"

    conciliacion_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    cuenta_bancaria_id = Column(Integer, ForeignKey("cuenta_bancaria.cuenta_bancaria_id"), nullable=False)

    fecha_desde = Column(Date, nullable=False)
    fecha_hasta = Column(Date, nullable=False)

    saldo_libros = Column(Numeric(14, 2), nullable=False)
    saldo_extracto = Column(Numeric(14, 2), nullable=False)
    diferencia = Column(Numeric(14, 2), nullable=False)

    estado = Column(String, default="borrador")  # borrador, finalizada

    created_by = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)

    detalles = relationship(
        "ConciliacionBancariaDetalle",
        back_populates="conciliacion",
        cascade="all, delete-orphan",
    )


class ConciliacionBancariaDetalle(Base):
    __tablename__ = "conciliacion_bancaria_detalle"

    conciliacion_detalle_id = Column(Integer, primary_key=True, index=True)
    conciliacion_id = Column(Integer, ForeignKey("conciliacion_bancaria.conciliacion_id"), nullable=False)
    movimiento_bancario_id = Column(Integer, ForeignKey("movimiento_bancario.movimiento_bancario_id"), nullable=False)

    tipo_diferencia = Column(String, nullable=True)  # en_transito, error_banco, error_libros, otro
    nota = Column(String, nullable=True)

    conciliacion = relationship("ConciliacionBancaria", back_populates="detalles")
