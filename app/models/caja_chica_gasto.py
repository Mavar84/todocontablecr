from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, TIMESTAMP
from database import Base


class CajaChicaGasto(Base):
    __tablename__ = "caja_chica_gasto"

    gasto_id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)
    caja_chica_id = Column(Integer, ForeignKey("caja_chica.caja_chica_id"), nullable=False)

    fecha = Column(Date, nullable=False)
    descripcion = Column(String, nullable=False)

    proveedor = Column(String, nullable=True)
    comprobante_numero = Column(String, nullable=True)     # factura física, tiquete, etc.

    monto = Column(Numeric(14, 2), nullable=False)
    moneda_id = Column(Integer, ForeignKey("moneda.moneda_id"), nullable=True)

    cuenta_contable_id = Column(Integer, ForeignKey("catalogo_cuenta.cuenta_id"), nullable=False)
    centro_costo_id = Column(Integer, ForeignKey("centro_costo.centro_costo_id"), nullable=True)

    estado = Column(String, nullable=False, default="registrado")
    # registrado, incluido_rendicion, aprobado, rechazado

    rendicion_id = Column(Integer, ForeignKey("caja_chica_rendicion.rendicion_id"), nullable=True)

    documento_url = Column(String, nullable=True)          # foto del tiquete, PDF, etc.

    creado_por = Column(Integer, nullable=True)
    creado_en = Column(TIMESTAMP, nullable=True)
    actualizado_por = Column(Integer, nullable=True)
    actualizado_en = Column(TIMESTAMP, nullable=True)
