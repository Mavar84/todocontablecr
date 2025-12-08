from pydantic import BaseModel
from typing import Optional


class CuentaBancariaBase(BaseModel):
    banco_nombre: str
    numero_cuenta: str
    descripcion: Optional[str] = None
    moneda_id: Optional[int] = None
    saldo_inicial: float = 0.0
    activa: bool = True


class CuentaBancariaCrear(CuentaBancariaBase):
    pass


class CuentaBancariaActualizar(BaseModel):
    banco_nombre: Optional[str] = None
    numero_cuenta: Optional[str] = None
    descripcion: Optional[str] = None
    moneda_id: Optional[int] = None
    saldo_inicial: Optional[float] = None
    activa: Optional[bool] = None


class CuentaBancaria(CuentaBancariaBase):
    cuenta_bancaria_id: int
    empresa_id: int

    class Config:
        from_attributes = True
