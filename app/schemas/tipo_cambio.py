from pydantic import BaseModel
from datetime import date
from typing import Optional


class TipoCambioBase(BaseModel):
    moneda_id: int
    fecha: date
    compra: Optional[float] = None
    venta: Optional[float] = None
    oficial: float


class TipoCambioCrear(TipoCambioBase):
    pass


class TipoCambio(TipoCambioBase):
    tipo_cambio_id: int

    class Config:
        from_attributes = True
