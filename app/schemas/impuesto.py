from pydantic import BaseModel
from typing import Optional


class ImpuestoBase(BaseModel):
    nombre: str
    tipo: str
    codigo_hacienda: Optional[str] = None
    tarifa: float
    es_por_defecto_iva: bool = False
    es_retencion: bool = False
    cuenta_contable_id: Optional[int] = None
    activo: bool = True


class ImpuestoCrear(ImpuestoBase):
    pass


class ImpuestoActualizar(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    codigo_hacienda: Optional[str] = None
    tarifa: Optional[float] = None
    es_por_defecto_iva: Optional[bool] = None
    es_retencion: Optional[bool] = None
    cuenta_contable_id: Optional[int] = None
    activo: Optional[bool] = None


class Impuesto(ImpuestoBase):
    impuesto_id: int
    empresa_id: Optional[int] = None

    class Config:
        from_attributes = True
