from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, TIMESTAMP
from database import Base


class CuentaCobrar(Base):
    __tablename__ = "cuenta_cobrar"

    cxc_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("cliente.cliente_id"), nullable=False)

    factura_id = Column(Integer, ForeignKey("factura_venta.factura_id"), nullable=True)

    descripcion = Column(String, nullable=True)
    fecha_emision = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=True)

    monto_original = Column(Numeric(14,2), nullable=False)
    saldo_actual = Column(Numeric(14,2), nullable=False)

    estado = Column(String, nullable=False)  # pendiente, parcial, cancelada, vencida

    comprobante_id = Column(Integer, ForeignKey("comprobante.comprobante_id"), nullable=True)

    created_by = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)


class CuentaCobrarMovimiento(Base):
    __tablename__ = "cuenta_cobrar_movimiento"

    cxc_mov_id = Column(Integer, primary_key=True, index=True)
    cxc_id = Column(Integer, ForeignKey("cuenta_cobrar.cxc_id"), nullable=False)

    fecha = Column(Date, nullable=False)
    tipo = Column(String, nullable=False)  # pago, nota_credito, ajuste, reversion
    monto = Column(Numeric(14,2), nullable=False)
    descripcion = Column(String, nullable=True)

    comprobante_id = Column(Integer, ForeignKey("comprobante.comprobante_id"), nullable=True)

    created_by = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
