from pydantic import BaseModel
from typing import Optional


class RetencionConfigBase(BaseModel):
    tipo: str
    nombre: str
    porcentaje: float
    base_minima: Optional[float] = None
    aplica_en_ventas: bool = False
    aplica_en_compras: bool = True
    cuenta_retencion_id: int
    activo: bool = True


class RetencionConfigCrear(RetencionConfigBase):
    pass


class RetencionConfigActualizar(BaseModel):
    nombre: Optional[str] = None
    porcentaje: Optional[float] = None
    base_minima: Optional[float] = None
    aplica_en_ventas: Optional[bool] = None
    aplica_en_compras: Optional[bool] = None
    cuenta_retencion_id: Optional[int] = None
    activo: Optional[bool] = None


class RetencionConfig(RetencionConfigBase):
    retencion_config_id: int
    empresa_id: int

    class Config:
        from_attributes = True
