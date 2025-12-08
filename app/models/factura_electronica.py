from sqlalchemy import Column, Integer, String, ForeignKey, Date, TIMESTAMP
from database import Base


class FacturaElectronica(Base):
    __tablename__ = "factura_electronica"

    fe_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    factura_id = Column(Integer, ForeignKey("factura_venta.factura_id"), nullable=False)

    tipo_documento = Column(String, nullable=False)  # FE, NC, ND, TE, etc.
    clave = Column(String, nullable=False, unique=True)
    consecutivo = Column(String, nullable=False)

    fecha_generacion = Column(Date, nullable=False)
    fecha_envio = Column(Date, nullable=True)
    fecha_respuesta = Column(Date, nullable=True)

    xml_sin_firma = Column(String, nullable=True)
    xml_firmado = Column(String, nullable=True)
    xml_enviado = Column(String, nullable=True)
    xml_respuesta = Column(String, nullable=True)

    estado_hacienda = Column(String, nullable=False, default="pendiente")  # pendiente, enviado, aceptado, rechazado, error
    codigo_respuesta = Column(String, nullable=True)
    mensaje_respuesta = Column(String, nullable=True)

    creado_por = Column(Integer, nullable=True)
    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_por = Column(Integer, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)
