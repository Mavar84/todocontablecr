from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey
from database import Base


class TipoActivo(Base):
    __tablename__ = "tipo_activo"

    tipo_activo_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)

    vida_util_meses = Column(Integer, nullable=False)  # ej: 60 meses
    porcentaje_residual = Column(Numeric(5,2), nullable=False, default=0)  # ej: 10%

    cuenta_activo_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=False)
    cuenta_depreciacion_acumulada_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"))
    cuenta_gasto_depreciacion_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"))

    activo = Column(Boolean, default=True)
