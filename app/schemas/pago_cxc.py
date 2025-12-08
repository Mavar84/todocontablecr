from pydantic import BaseModel
from datetime import date
from typing import Optional


class PagoCXCBase(BaseModel):
    cxc_id: int
    fecha_pago: date
    moneda_id: Optional[int] = None
    monto: float
    tipo_pago: Optional[str] = None
    referencia: Optional[str] = None
    comprobante_id: Optional[int] = None


class PagoCXCCrear(PagoCXCBase):
    pass


class PagoCXC(PagoCXCBase):
    pago_cxc_id: int
    empresa_id: int

    class Config:
        from_attributes = True
