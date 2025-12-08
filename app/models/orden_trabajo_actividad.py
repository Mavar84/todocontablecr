from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, TIMESTAMP
from database import Base


class OrdenTrabajoActividad(Base):
    __tablename__ = "orden_trabajo_actividad"

    actividad_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    orden_trabajo_id = Column(Integer, ForeignKey("orden_trabajo.orden_trabajo_id"), nullable=False)

    fecha = Column(Date, nullable=False)
    descripcion = Column(String, nullable=False)

    horas = Column(Numeric(10, 2), nullable=True)
    tarifa_hora = Column(Numeric(14, 4), nullable=True)
    costo_mano_obra = Column(Numeric(14, 2), nullable=False, default=0)

    costo_indirecto = Column(Numeric(14, 2), nullable=False, default=0)

    cuenta_contable_mo_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=True)
    cuenta_contable_indirectos_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=True)

    comentario = Column(String, nullable=True)

    creado_por = Column(Integer, nullable=True)
    creado_en = Column(TIMESTAMP, nullable=True)
