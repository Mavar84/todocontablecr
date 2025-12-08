from datetime import date
from pydantic import BaseModel
from typing import Optional


class CxPBase(BaseModel):
    proveedor_id: int
    descripcion: Optional[str] = None
    fecha_emision: date
    fecha_vencimiento: Optional[date] = None
    monto_original: float


class CxPCreate(CxPBase):
    comprobante_id: Optional[int] = None
    orden_compra_id: Optional[int] = None


class CxPUpdate(BaseModel):
    descripcion: Optional[str] = None
    fecha_vencimiento: Optional[date] = None


class CxP(BaseModel):
    cxp_id: int
    empresa_id: int
    proveedor_id: int
    descripcion: Optional[str]
    fecha_emision: date
    fecha_vencimiento: Optional[date]
    monto_original: float
    saldo_actual: float
    estado: str

    class Config:
        from_attributes = True


# --- Movimientos ---
class CxPMovBase(BaseModel):
    fecha: date
    tipo: str  # pago, nota_debito, nota_credito, ajuste, reversion
    monto: float
    descripcion: Optional[str] = None


class CxPMovCreate(CxPMovBase):
    comprobante_id: Optional[int] = None


class CxPMov(BaseModel):
    cxp_mov_id: int
    cxp_id: int
    fecha: date
    tipo: str
    monto: float
    descripcion: Optional[str]

    class Config:
        from_attributes = True
