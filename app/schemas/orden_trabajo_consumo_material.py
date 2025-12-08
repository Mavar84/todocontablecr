from pydantic import BaseModel
from typing import Optional
from datetime import date


class OrdenTrabajoConsumoMaterialBase(BaseModel):
    orden_trabajo_id: int
    producto_id: int
    bodega_id: Optional[int] = None
    fecha_consumo: date
    cantidad: float
    costo_unitario: float
    costo_total: float
    movimiento_inventario_id: Optional[int] = None
    comentario: Optional[str] = None


class OrdenTrabajoConsumoMaterialCrear(OrdenTrabajoConsumoMaterialBase):
    pass


class OrdenTrabajoConsumoMaterial(OrdenTrabajoConsumoMaterialBase):
    consumo_id: int
    empresa_id: int

    class Config:
        from_attributes = True
