from datetime import date
from pydantic import BaseModel
from typing import Optional


class InventarioSaldo(BaseModel):
    inventario_saldo_id: int
    empresa_id: int
    producto_id: int
    bodega_id: int
    cantidad: float
    costo_promedio: float

    class Config:
        from_attributes = True


class MovimientoInventarioBase(BaseModel):
    producto_id: int
    bodega_id: int
    fecha: date
    tipo: str        # entrada, salida
    referencia: Optional[str] = None
    origen: Optional[str] = None
    origen_id: Optional[int] = None
    cantidad: float
    costo_unitario: float
    comprobante_id: Optional[int] = None


class MovimientoInventarioCrear(MovimientoInventarioBase):
    pass


class MovimientoInventario(MovimientoInventarioBase):
    movimiento_inventario_id: int
    costo_total: float

    class Config:
        from_attributes = True
