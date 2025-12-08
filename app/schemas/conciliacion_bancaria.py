from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class ConciliacionDetalleBase(BaseModel):
    movimiento_bancario_id: int
    tipo_diferencia: Optional[str] = None
    nota: Optional[str] = None


class ConciliacionDetalle(ConciliacionDetalleBase):
    conciliacion_detalle_id: int

    class Config:
        from_attributes = True


class ConciliacionCrear(BaseModel):
    cuenta_bancaria_id: int
    fecha_desde: date
    fecha_hasta: date
    saldo_extracto: float
    movimientos: List[ConciliacionDetalleBase] = []


class Conciliacion(BaseModel):
    conciliacion_id: int
    empresa_id: int
    cuenta_bancaria_id: int
    fecha_desde: date
    fecha_hasta: date
    saldo_libros: float
    saldo_extracto: float
    diferencia: float
    estado: str
    detalles: List[ConciliacionDetalle] = []

    class Config:
        from_attributes = True
