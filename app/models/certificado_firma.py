from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, Date
from database import Base


class CertificadoFirma(Base):
    __tablename__ = "certificado_firma"

    certificado_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    nombre = Column(String, nullable=False)
    archivo_p12_base64 = Column(String, nullable=False)
    pin = Column(String, nullable=False)

    fecha_vencimiento = Column(Date, nullable=True)
    activo = Column(Boolean, default=True)

    creado_por = Column(Integer, nullable=True)
    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_por = Column(Integer, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)
