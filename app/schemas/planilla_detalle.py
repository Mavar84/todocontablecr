from pydantic import BaseModel
from typing import Optional


class PlanillaDetalleOut(BaseModel):
    detalle_id: int
    planilla_id: int
    empleado_id: int

    salario_base: float
    horas_extra: float
    monto_horas_extra: float

    incapacidades: float
    vacaciones: float
    bonos: float

    total_devengado: float

    total_obrero: float
    total_patrono: float
    renta: float

    neto_pagar: float

    class Config:
        from_attributes = True
