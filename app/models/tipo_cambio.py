from sqlalchemy import Column, Integer, Date, ForeignKey, Numeric, UniqueConstraint
from database import Base


class TipoCambio(Base):
    __tablename__ = "tipo_cambio"

    tipo_cambio_id = Column(Integer, primary_key=True, index=True)
    moneda_id = Column(Integer, ForeignKey("moneda.moneda_id"), nullable=False)

    fecha = Column(Date, nullable=False)
    compra = Column(Numeric(18,6), nullable=True)   # si desea manejar compra / venta
    venta = Column(Numeric(18,6), nullable=True)
    oficial = Column(Numeric(18,6), nullable=False) # tipo que se usará para revaluación

    __table_args__ = (
        UniqueConstraint("moneda_id", "fecha", name="uq_tipo_cambio_moneda_fecha"),
    )
