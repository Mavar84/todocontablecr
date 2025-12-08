from pydantic import BaseModel
from typing import Optional


class RetencionAplicadaBase(BaseModel):
    retencion_config_id: int
    origen_tipo: str
    origen_id: int
    monto_base: float
    monto_retencion: float
    comprobante_id: Optional[int] = None


class RetencionAplicadaCrear(RetencionAplicadaBase):
    pass


class RetencionAplicada(RetencionAplicadaBase):
    retencion_aplicada_id: int
    empresa_id: int

    class Config:
        from_attributes = True
