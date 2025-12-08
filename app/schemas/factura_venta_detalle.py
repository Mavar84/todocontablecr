from pydantic import BaseModel
from typing import Optional


class FacturaVentaDetalleBase(BaseModel):
    producto_id: Optional[int] = None
    descripcion: Optional[str] = None
    cantidad: float
    precio_unitario: float
    descuento: float = 0.0
    impuesto: float = 0.0
    cuenta_ingreso_id: Optional[int] = None


class FacturaVentaDetalleCreate(FacturaVentaDetalleBase):
    pass


class FacturaVentaDetalle(FacturaVentaDetalleBase):
    factura_detalle_id: int

    class Config:
        from_attributes = True
