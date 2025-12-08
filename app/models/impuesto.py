from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, TIMESTAMP
from database import Base


class Impuesto(Base):
    __tablename__ = "impuesto"

    impuesto_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=True)

    nombre = Column(String, nullable=False)          # IVA 13%, IVA 4%, Exento, Retención Renta 2%, etc.
    tipo = Column(String, nullable=False)            # IVA, EXENTO, RETENCION_IVA, RETENCION_RENTA, OTRO
    codigo_hacienda = Column(String, nullable=True)  # código de impuesto según Hacienda para XML
    tarifa = Column(Numeric(6,3), nullable=False, default=0)    # porcentaje, por ejemplo 13.000

    es_por_defecto_iva = Column(Boolean, default=False)
    es_retencion = Column(Boolean, default=False)

    activo = Column(Boolean, default=True)

    cuenta_contable_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=True)

    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)
