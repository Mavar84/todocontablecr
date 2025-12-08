from pydantic import BaseModel
from typing import Optional


class TipoActivoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    vida_util_meses: int
    porcentaje_residual: float
    cuenta_activo_id: int
    cuenta_depreciacion_acumulada_id: int
    cuenta_gasto_depreciacion_id: int


class TipoActivoCrear(TipoActivoBase):
    pass


class TipoActivoActualizar(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    vida_util_meses: Optional[int] = None
    porcentaje_residual: Optional[float] = None
    cuenta_activo_id: Optional[int] = None
    cuenta_depreciacion_acumulada_id: Optional[int] = None
    cuenta_gasto_depreciacion_id: Optional[int] = None


class TipoActivo(TipoActivoBase):
    tipo_activo_id: int
    empresa_id: int

    class Config:
        from_attributes = True
