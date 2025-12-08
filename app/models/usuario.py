from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    usuario_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    clave_hash = Column(String, nullable=False)
    activo = Column(Boolean, default=True)

    fecha_creacion = Column(TIMESTAMP)
    ultima_sesion = Column(TIMESTAMP)

    created_by = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_by = Column(Integer)
    updated_at = Column(TIMESTAMP)
