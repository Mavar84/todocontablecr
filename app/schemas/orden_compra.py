from datetime import date
from pydantic import BaseModel
from typing import Optional, List
from .orden_compra_detalle import (
    OrdenCompraDetalleCreate,
    OrdenCompraDetalle,
)


class OrdenCompraBase(BaseModel):
    proveedor_id: int
    fecha: date
    moneda_id: Optional[int] = None
    numero: Optional[str] = None
    bodega_entrada_id: Optional[int] = None


class OrdenCompraCreate(OrdenCompraBase):
    detalles: List[OrdenCompraDetalleCreate]


class OrdenCompra(OrdenCompraBase):
    orden_compra_id: int
    empresa_id: int
    subtotal: float
    descuento_total: float
    impuesto_total: float
    total: float
    estado: str
    detalles: List[OrdenCompraDetalle]

    class Config:
        from_attributes = True
