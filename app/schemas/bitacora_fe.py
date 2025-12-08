from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BitacoraFEBase(BaseModel):
    tipo: str
    referencia_id: int
    accion: str
    detalle: Optional[str] = None
    estado: Optional[str] = None


class BitacoraFECrear(BitacoraFEBase):
    pass


class BitacoraFE(BitacoraFEBase):
    bitacora_fe_id: int
    empresa_id: int
    creado_en: Optional[datetime] = None

    class Config:
        from_attributes = True
