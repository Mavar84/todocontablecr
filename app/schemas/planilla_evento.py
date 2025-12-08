from pydantic import BaseModel
from typing import Optional
from datetime import date


class PlanillaEventoBase(BaseModel):
    empleado_id: int
    fecha: date
    tipo: str          # horas_extra, vacaciones, incapacidad, permiso, bono
    cantidad: float
    monto: Optional[float] = None
    comentario: Optional[str] = None


class PlanillaEventoCrear(PlanillaEventoBase):
    pass


class PlanillaEventoOut(PlanillaEventoBase):
    evento_id: int
    empresa_id: int

    class Config:
        from_attributes = True
