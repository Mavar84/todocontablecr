from pydantic import BaseModel
from typing import Optional


class CajaChicaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    moneda_id: Optional[int] = None
    monto_maximo: float
    saldo_inicial: float
    saldo_actual: float
    cuenta_contable_id: Optional[int] = None
    responsable_usuario_id: Optional[int] = None
    activa: bool = True


class CajaChicaCrear(CajaChicaBase):
    pass


class CajaChicaActualizar(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    moneda_id: Optional[int] = None
    monto_maximo: Optional[float] = None
    cuenta_contable_id: Optional[int] = None
    responsable_usuario_id: Optional[int] = None
    activa: Optional[bool] = None
    # saldo_actual y saldo_inicial no se tocan libremente desde API normal


class CajaChica(CajaChicaBase):
    caja_chica_id: int
    empresa_id: int

    class Config:
        from_attributes = True
