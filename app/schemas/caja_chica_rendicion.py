from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class CajaChicaRendicionBase(BaseModel):
    caja_chica_id: int
    fecha_inicio: date
    fecha_fin: date
    fecha_rendicion: date
    estado: str = "borrador"
    total_gastos: float = 0.0
    total_reponer: float = 0.0
    observaciones: Optional[str] = None
    comprobante_id: Optional[int] = None


class CajaChicaRendicionCrear(CajaChicaRendicionBase):
    pass


class CajaChicaRendicionActualizar(BaseModel):
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    fecha_rendicion: Optional[date] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None
    comprobante_id: Optional[int] = None
    # total_gastos y total_reponer se recalculan, no se modifican directo


class CajaChicaRendicion(CajaChicaRendicionBase):
    rendicion_id: int
    empresa_id: int

    class Config:
        from_attributes = True
