from pydantic import BaseModel
from typing import List


class ConciliacionMovimientoExtracto(BaseModel):
    extracto_movimiento_id: int
    monto: float


class ConciliacionGenerar(BaseModel):
    conciliacion_id: int
    movimientos_extracto: List[ConciliacionMovimientoExtracto]
