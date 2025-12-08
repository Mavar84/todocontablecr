from pydantic import BaseModel
from typing import Literal


class ConciliacionDetalleBase(BaseModel):
    conciliacion_id: int
    tipo_origen: Literal["EXTRACTO", "MOV_CONTABLE", "PAGO_CXC", "PAGO_CXP", "OTRO"]
    origen_id: int
    monto: float
    naturaleza: Literal["CONCILIADO", "PENDIENTE_LIBROS", "PENDIENTE_BANCO"]


class ConciliacionDetalleCrear(ConciliacionDetalleBase):
    pass


class ConciliacionDetalle(ConciliacionDetalleBase):
    conciliacion_detalle_id: int
    empresa_id: int

    class Config:
        from_attributes = True
