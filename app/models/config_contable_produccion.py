from sqlalchemy import Column, Integer, ForeignKey
from database import Base


class ConfigContableProduccion(Base):
    __tablename__ = "config_contable_produccion"

    config_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    cuenta_pip_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=False)  # Producción en proceso
    cuenta_mp_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=False)   # Inventario de MP
    cuenta_mo_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=False)   # Mano de obra aplicada
    cuenta_cif_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=False)  # Costos indirectos
    cuenta_pt_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=False)   # Producto terminado
