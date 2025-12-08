from pydantic import BaseModel
from typing import Optional
from datetime import date


class OrdenTrabajoActividadBase(BaseModel):
    orden_trabajo_id: int
    fecha: date
    descripcion: str
    horas: Optional[float] = None
    tarifa_hora: Optional[float] = None
    costo_mano_obra: float
    costo_indirecto: float = 0.0
    cuenta_contable_mo_id: Optional[int] = None
    cuenta_contable_indirectos_id: Optional[int] = None
    comentario: Optional[str] = None


class OrdenTrabajoActividadCrear(OrdenTrabajoActividadBase):
    pass


class OrdenTrabajoActividad(OrdenTrabajoActividadBase):
    actividad_id: int
    empresa_id: int

    class Config:
        from_attributes = True
