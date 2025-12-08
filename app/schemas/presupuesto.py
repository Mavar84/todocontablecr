from pydantic import BaseModel
from typing import Optional


class PresupuestoBase(BaseModel):
    nombre: str
    anio: int
    periodo: Optional[str] = "ANUAL"
    descripcion: Optional[str] = None
    estado: str = "borrador"


class PresupuestoCrear(PresupuestoBase):
    pass


class PresupuestoActualizar(BaseModel):
    nombre: Optional[str] = None
    periodo: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None


class Presupuesto(PresupuestoBase):
    presupuesto_id: int
    empresa_id: int

    class Config:
        from_attributes = True
