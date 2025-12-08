from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base


class Comprobante(Base):
    __tablename__ = "comprobante"

    comprobante_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    periodo_id = Column(Integer, ForeignKey("periodo_contable.periodo_id"), nullable=True)
    tipo_comprobante_id = Column(Integer, ForeignKey("tipo_comprobante.tipo_comprobante_id"), nullable=True)

    numero = Column(String, nullable=True)
    fecha = Column(Date, nullable=False)
    descripcion = Column(String, nullable=True)

    estado = Column(String, default="borrador")  # borrador, publicado, anulado

    moneda_id = Column(Integer, ForeignKey("moneda.moneda_id"), nullable=True)
    tipo_cambio_usado = Column(Numeric(14,4), nullable=True)

    creado_por = Column(Integer, ForeignKey("usuario.usuario_id"), nullable=True)
    fecha_creacion = Column(TIMESTAMP)
    updated_by = Column(Integer)
    updated_at = Column(TIMESTAMP)

    movimientos = relationship("Movimiento", back_populates="comprobante", cascade="all, delete-orphan")
