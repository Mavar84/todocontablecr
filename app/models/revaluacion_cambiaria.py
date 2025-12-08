from sqlalchemy import Column, Integer, Date, ForeignKey, Numeric, String, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base


class RevaluacionCambiaria(Base):
    __tablename__ = "revaluacion_cambiaria"

    revaluacion_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    fecha = Column(Date, nullable=False)
    moneda_id = Column(Integer, ForeignKey("moneda.moneda_id"), nullable=False)

    tipo_cambio_anterior = Column(Numeric(18,6), nullable=False)
    tipo_cambio_nuevo = Column(Numeric(18,6), nullable=False)

    total_ajuste = Column(Numeric(18,2), nullable=False)      # suma de todos los ajustes
    estado = Column(String, default="borrador")               # borrador, aplicado

    comprobante_id = Column(Integer, ForeignKey("comprobante.comprobante_id"), nullable=True)

    created_by = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)

    detalles = relationship(
        "RevaluacionCambiariaDetalle",
        back_populates="revaluacion",
        cascade="all, delete-orphan"
    )


class RevaluacionCambiariaDetalle(Base):
    __tablename__ = "revaluacion_cambiaria_detalle"

    revaluacion_detalle_id = Column(Integer, primary_key=True, index=True)
    revaluacion_id = Column(Integer, ForeignKey("revaluacion_cambiaria.revaluacion_id"), nullable=False)

    cuenta_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=False)

    saldo_moneda = Column(Numeric(18,6), nullable=False)       # saldo en moneda extranjera
    valor_anterior = Column(Numeric(18,2), nullable=False)     # saldo en moneda local con tipo anterior
    valor_nuevo = Column(Numeric(18,2), nullable=False)        # saldo en moneda local con tipo nuevo
    ajuste = Column(Numeric(18,2), nullable=False)             # valor_nuevo - valor_anterior

    revaluacion = relationship("RevaluacionCambiaria", back_populates="detalles")
