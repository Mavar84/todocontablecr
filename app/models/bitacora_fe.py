from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from database import Base


class BitacoraFE(Base):
    __tablename__ = "bitacora_fe"

    bitacora_fe_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    tipo = Column(String, nullable=False)  # emision, recepcion
    referencia_id = Column(Integer, nullable=False)  # fe_id o recepcion_id
    accion = Column(String, nullable=False)
    detalle = Column(String, nullable=True)
    estado = Column(String, nullable=True)

    creado_por = Column(Integer, nullable=True)
    creado_en = Column(TIMESTAMP, nullable=True)
