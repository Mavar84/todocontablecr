from pydantic import BaseModel
from datetime import date
from typing import Optional


class DepreciacionActivoBase(BaseModel):
    fecha: date
    monto: float
    comprobante_id: Optional[int] = None


class DepreciacionActivoCrear(DepreciacionActivoBase):
    pass


class DepreciacionActivo(BaseModel):
    depreciacion_id: int
    activo_id: int
    fecha: date
    monto: float

    class Config:
        from_attributes = True
