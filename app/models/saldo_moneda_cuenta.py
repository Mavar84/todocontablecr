from sqlalchemy import Column, Integer, ForeignKey, Numeric, UniqueConstraint
from database import Base


class SaldoMonedaCuenta(Base):
    __tablename__ = "saldo_moneda_cuenta"

    saldo_moneda_cuenta_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    cuenta_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=False)
    moneda_id = Column(Integer, ForeignKey("moneda.moneda_id"), nullable=False)

    saldo_moneda = Column(Numeric(18,6), nullable=False)

    __table_args__ = (
        UniqueConstraint("empresa_id", "cuenta_id", "moneda_id", name="uq_saldo_moneda_cuenta"),
    )
