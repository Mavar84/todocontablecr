from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, TIMESTAMP
from database import Base


class CuentaPagar(Base):
    __tablename__ = "cuenta_pagar"

    cxp_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    proveedor_id = Column(Integer, ForeignKey("proveedor.proveedor_id"), nullable=False)

    orden_compra_id = Column(Integer, ForeignKey("orden_compra.orden_compra_id"), nullable=True)

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


class CuentaPagarMovimiento(Base):
    __tablename__ = "cuenta_pagar_movimiento"

    cxp_mov_id = Column(Integer, primary_key=True, index=True)
    cxp_id = Column(Integer, ForeignKey("cuenta_pagar.cxp_id"), nullable=False)

    fecha = Column(Date, nullable=False)
    tipo = Column(String, nullable=False)  # pago, nota_debito, nota_credito, ajuste, reversion
    monto = Column(Numeric(14,2), nullable=False)
    descripcion = Column(String, nullable=True)

    comprobante_id = Column(Integer, ForeignKey("comprobante.comprobante_id"), nullable=True)

    created_by = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
