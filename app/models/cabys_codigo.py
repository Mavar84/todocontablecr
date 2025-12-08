from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from database import Base


class CabysCodigo(Base):
    __tablename__ = "cabys_codigo"

    cabys_id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, nullable=False, unique=True)        # 13 dígitos
    descripcion = Column(String, nullable=False)
    activo = Column(Boolean, default=True)

    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)
