from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, TIMESTAMP
from database import Base


class CajaChica(Base):
    __tablename__ = "caja_chica"

    caja_chica_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    nombre = Column(String, nullable=False)                   # Caja chica administración
    descripcion = Column(String, nullable=True)

    moneda_id = Column(Integer, ForeignKey("moneda.moneda_id"), nullable=True)

    monto_maximo = Column(Numeric(14, 2), nullable=False, default=0)    # tope autorizado
    saldo_inicial = Column(Numeric(14, 2), nullable=False, default=0)
    saldo_actual = Column(Numeric(14, 2), nullable=False, default=0)

    cuenta_contable_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=True)

    responsable_usuario_id = Column(Integer, nullable=True)    # FK a usuarios si se desea luego

    activa = Column(Boolean, default=True)

    creado_por = Column(Integer, nullable=True)
    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_por = Column(Integer, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)
