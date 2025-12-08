from pydantic import BaseModel
from typing import Optional


class OrdenTrabajoMaterialPlanBase(BaseModel):
    orden_trabajo_id: int
    producto_id: int
    bodega_id: Optional[int] = None
    cantidad_planeada: float
    unidad: Optional[str] = None
    costo_unitario_estimado: Optional[float] = None
    costo_total_estimado: Optional[float] = None
    comentario: Optional[str] = None


class OrdenTrabajoMaterialPlanCrear(OrdenTrabajoMaterialPlanBase):
    pass


class OrdenTrabajoMaterialPlanActualizar(BaseModel):
    cantidad_planeada: Optional[float] = None
    costo_unitario_estimado: Optional[float] = None
    costo_total_estimado: Optional[float] = None
    comentario: Optional[str] = None


class OrdenTrabajoMaterialPlan(OrdenTrabajoMaterialPlanBase):
    material_plan_id: int
    empresa_id: int

    class Config:
        from_attributes = True
