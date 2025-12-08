from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, TIMESTAMP
from database import Base


class CajaChicaRendicion(Base):
    __tablename__ = "caja_chica_rendicion"

    rendicion_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    caja_chica_id = Column(Integer, ForeignKey("caja_chica.caja_chica_id"), nullable=False)

    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    fecha_rendicion = Column(Date, nullable=False)

    estado = Column(String, nullable=False, default="borrador")
    # borrador, enviada, aprobada, contabilizada

    total_gastos = Column(Numeric(14, 2), nullable=False, default=0)
    total_reponer = Column(Numeric(14, 2), nullable=False, default=0)

    observaciones = Column(String, nullable=True)

    comprobante_id = Column(Integer, ForeignKey("comprobante.comprobante_id"), nullable=True)

    creado_por = Column(Integer, nullable=True)
    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_por = Column(Integer, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)
