from sqlalchemy import Column, Integer, ForeignKey, Numeric, UniqueConstraint
from database import Base


class InventarioSaldo(Base):
    __tablename__ = "inventario_saldo"

    inventario_saldo_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("producto.producto_id"), nullable=False)
    bodega_id = Column(Integer, ForeignKey("bodega.bodega_id"), nullable=False)

    cantidad = Column(Numeric(14, 4), nullable=False, default=0)
    costo_promedio = Column(Numeric(14, 4), nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("empresa_id", "producto_id", "bodega_id", name="uq_inv_saldo_emp_prod_bod"),
    )
