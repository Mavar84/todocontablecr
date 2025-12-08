from datetime import date
from pydantic import BaseModel
from typing import Optional


class CxCBase(BaseModel):
    cliente_id: int
    descripcion: Optional[str] = None
    fecha_emision: date
    fecha_vencimiento: Optional[date] = None
    monto_original: float


class CxCCreate(CxCBase):
    comprobante_id: Optional[int] = None
    factura_id: Optional[int] = None


class CxCUpdate(BaseModel):
    descripcion: Optional[str] = None
    fecha_vencimiento: Optional[date] = None


class CxC(BaseModel):
    cxc_id: int
    empresa_id: int
    cliente_id: int
    descripcion: Optional[str] = None
    fecha_emision: date
    fecha_vencimiento: Optional[date]
    monto_original: float
    saldo_actual: float
    estado: str

    class Config:
        from_attributes = True


# --- Movimientos ---
class CxCMovBase(BaseModel):
    fecha: date
    tipo: str  # pago, nota_credito, ajuste, reversion
    monto: float
    descripcion: Optional[str] = None


class CxCMovCreate(CxCMovBase):
    comprobante_id: Optional[int] = None


class CxCMov(BaseModel):
    cxc_mov_id: int
    cxc_id: int
    fecha: date
    tipo: str
    monto: float
    descripcion: Optional[str]

    class Config:
        from_attributes = True
