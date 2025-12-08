from pydantic import BaseModel
from typing import Optional
from datetime import date


class PlanillaBase(BaseModel):
    periodo: str                # ejemplo: 2025-02-Quincena1
    fecha_pago: date


class PlanillaCrear(PlanillaBase):
    pass


class PlanillaOut(PlanillaBase):
    planilla_id: int
    empresa_id: int
    estado: str
    total_salarios: float
    total_obrero: float
    total_patrono: float
    total_renta: float
    total_neto: float

    class Config:
        from_attributes = True
