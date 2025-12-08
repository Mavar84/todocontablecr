from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class RevaluacionDetalleBase(BaseModel):
    cuenta_id: int
    saldo_moneda: float
    valor_anterior: float
    valor_nuevo: float
    ajuste: float


class RevaluacionDetalle(RevaluacionDetalleBase):
    revaluacion_detalle_id: int

    class Config:
        from_attributes = True


class RevaluacionCambiariaCrear(BaseModel):
    moneda_id: int
    fecha: date
    tipo_cambio_anterior: float
    tipo_cambio_nuevo: float
    comprobante_id: Optional[int] = None


class RevaluacionCambiaria(BaseModel):
    revaluacion_id: int
    empresa_id: int
    moneda_id: int
    fecha: date
    tipo_cambio_anterior: float
    tipo_cambio_nuevo: float
    total_ajuste: float
    estado: str
    comprobante_id: Optional[int] = None
    detalles: List[RevaluacionDetalle] = []

    class Config:
        from_attributes = True
