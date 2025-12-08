from datetime import date
from pydantic import BaseModel
from typing import Optional, List
from .depreciacion_activo import DepreciacionActivo


class ActivoFijoBase(BaseModel):
    tipo_activo_id: int
    nombre: str
    descripcion: Optional[str] = None
    fecha_compra: date
    costo: float
    valor_residual: float
    vida_util_meses: int


class ActivoFijoCrear(ActivoFijoBase):
    comprobante_id: Optional[int] = None


class ActivoFijoActualizar(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None


class ActivoFijo(ActivoFijoBase):
    activo_id: int
    empresa_id: int
    depreciacion_acumulada: float
    valor_en_libros: float
    estado: str
    depreciaciones: List[DepreciacionActivo] = []

    class Config:
        from_attributes = True
