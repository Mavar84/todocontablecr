from pydantic import BaseModel
from typing import Optional


class FacturaCompraDetalleBase(BaseModel):
    producto_id: Optional[int] = None
    descripcion: Optional[str] = None
    cantidad: float
    costo_unitario: float
    descuento: float = 0.0
    impuesto: float = 0.0
    cuenta_gasto_id: Optional[int] = None


class FacturaCompraDetalleCreate(FacturaCompraDetalleBase):
    pass


class FacturaCompraDetalle(FacturaCompraDetalleBase):
    factura_compra_detalle_id: int

    class Config:
        from_attributes = True
