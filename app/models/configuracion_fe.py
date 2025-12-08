from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from database import Base


class ConfiguracionFE(Base):
    __tablename__ = "configuracion_fe"

    configuracion_fe_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False, unique=True)

    tipo_ambiente = Column(String, nullable=False)  # pruebas, produccion
    cedula_emisor = Column(String, nullable=False)
    nombre_comercial = Column(String, nullable=True)
    correo_notificacion = Column(String, nullable=True)

    sucursal = Column(String, nullable=True)
    terminal = Column(String, nullable=True)

    codigo_pais_telefono = Column(String, nullable=True)
    telefono = Column(String, nullable=True)

    usuario_api = Column(String, nullable=True)
    clave_api = Column(String, nullable=True)

    certificado_activo_id = Column(Integer, ForeignKey("certificado_firma.certificado_id"), nullable=True)

    activo = Column(Boolean, default=True)

    creado_por = Column(Integer, nullable=True)
    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_por = Column(Integer, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)
