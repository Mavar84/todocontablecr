from datetime import date
from pydantic import BaseModel
from typing import Optional, List
from .factura_compra_detalle import (
    FacturaCompraDetalleCreate,
    FacturaCompraDetalle,
)


class FacturaCompraBase(BaseModel):
    proveedor_id: int
    fecha: date
    moneda_id: Optional[int] = None
    numero: Optional[str] = None
    bodega_entrada_id: Optional[int] = None
    orden_compra_id: Optional[int] = None


class FacturaCompraCreate(FacturaCompraBase):
    detalles: List[FacturaCompraDetalleCreate]
    es_credito: bool = True
    descripcion_cxp: Optional[str] = None
    fecha_vencimiento: Optional[date] = None
    comprobante_id: Optional[int] = None


class FacturaCompra(FacturaCompraBase):
    factura_compra_id: int
    empresa_id: int
    subtotal: float
    descuento_total: float
    impuesto_total: float
    total: float
    estado: Optional[str] = None
    detalles: List[FacturaCompraDetalle]

    class Config:
        from_attributes = True
