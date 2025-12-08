from pydantic import BaseModel
from typing import Optional
from datetime import date


class CajaChicaGastoBase(BaseModel):
    caja_chica_id: int
    fecha: date
    descripcion: str
    proveedor: Optional[str] = None
    comprobante_numero: Optional[str] = None
    monto: float
    moneda_id: Optional[int] = None
    cuenta_contable_id: int
    centro_costo_id: Optional[int] = None
    estado: str = "registrado"
    documento_url: Optional[str] = None


class CajaChicaGastoCrear(CajaChicaGastoBase):
    pass


class CajaChicaGastoActualizar(BaseModel):
    descripcion: Optional[str] = None
    proveedor: Optional[str] = None
    comprobante_numero: Optional[str] = None
    centro_costo_id: Optional[int] = None
    estado: Optional[str] = None
    documento_url: Optional[str] = None
    # no permitimos cambiar monto ni caja_chica_id por simplicidad de saldo


class CajaChicaGasto(CajaChicaGastoBase):
    gasto_id: int
    empresa_id: int
    rendicion_id: Optional[int] = None

    class Config:
        from_attributes = True
