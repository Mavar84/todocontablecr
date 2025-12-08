from pydantic import BaseModel
from typing import Optional


class PresupuestoLineaBase(BaseModel):
    cuenta_id: int
    centro_costo_id: Optional[int] = None
    mes: Optional[int] = None    # 1-12 o None para anual
    monto_presupuestado: float
    comentario: Optional[str] = None


class PresupuestoLineaCrear(PresupuestoLineaBase):
    presupuesto_id: int


class PresupuestoLineaActualizar(BaseModel):
    mes: Optional[int] = None
    monto_presupuestado: Optional[float] = None
    comentario: Optional[str] = None


class PresupuestoLinea(PresupuestoLineaBase):
    linea_id: int
    presupuesto_id: int
    empresa_id: int

    class Config:
        from_attributes = True
