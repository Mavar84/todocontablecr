from pydantic import BaseModel
from datetime import date
from typing import Optional


class EmpleadoSalarioHistBase(BaseModel):
    salario_base: float
    fecha_inicio: date
    fecha_fin: Optional[date] = None


class EmpleadoSalarioHistCrear(EmpleadoSalarioHistBase):
    empleado_id: int


class EmpleadoSalarioHistOut(EmpleadoSalarioHistBase):
    hist_id: int

    class Config:
        from_attributes = True
