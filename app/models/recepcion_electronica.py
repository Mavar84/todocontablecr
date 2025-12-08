from sqlalchemy import Column, Integer, String, ForeignKey, Date, TIMESTAMP
from database import Base


class RecepcionElectronica(Base):
    __tablename__ = "recepcion_electronica"

    recepcion_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    factura_compra_id = Column(Integer, ForeignKey("factura_compra.factura_compra_id"), nullable=True)

    clave = Column(String, nullable=False)
    consecutivo_emisor = Column(String, nullable=True)
    cedula_emisor = Column(String, nullable=True)

    fecha_recepcion = Column(Date, nullable=False)
    fecha_respuesta = Column(Date, nullable=True)

    xml_original = Column(String, nullable=False)
    xml_aceptacion = Column(String, nullable=True)

    estado_respuesta = Column(String, nullable=False, default="pendiente")  # pendiente, aceptado, aceptado_parcial, rechazado
    mensaje_respuesta = Column(String, nullable=True)

    creado_por = Column(Integer, nullable=True)
    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_por = Column(Integer, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)
