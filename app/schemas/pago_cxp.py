from pydantic import BaseModel
from datetime import date
from typing import Optional


class PagoCXPBase(BaseModel):
    cxp_id: int
    fecha_pago: date
    moneda_id: Optional[int] = None
    monto: float
    tipo_pago: Optional[str] = None
    referencia: Optional[str] = None
    comprobante_id: Optional[int] = None


class PagoCXPCrear(PagoCXPBase):
    pass


class PagoCXP(PagoCXPBase):
    pago_cxp_id: int
    empresa_id: int

    class Config:
        from_attributes = True
