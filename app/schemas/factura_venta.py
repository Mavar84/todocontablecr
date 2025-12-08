from datetime import date
from pydantic import BaseModel
from typing import Optional, List
from .factura_venta_detalle import (
    FacturaVentaDetalleCreate,
    FacturaVentaDetalle,
)


class FacturaVentaBase(BaseModel):
    cliente_id: int
    fecha: date
    moneda_id: Optional[int] = None
    numero: Optional[str] = None
    bodega_salida_id: Optional[int] = None


class FacturaVentaCreate(FacturaVentaBase):
    detalles: List[FacturaVentaDetalleCreate]
    es_credito: bool = True
    descripcion_cxc: Optional[str] = None
    fecha_vencimiento: Optional[date] = None
    comprobante_id: Optional[int] = None


class FacturaVenta(FacturaVentaBase):
    factura_id: int
    empresa_id: int
    subtotal: float
    descuento_total: float
    impuesto_total: float
    total: float
    estado: Optional[str] = None
    detalles: List[FacturaVentaDetalle]

    class Config:
        from_attributes = True
