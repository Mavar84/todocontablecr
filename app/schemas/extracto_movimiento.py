from pydantic import BaseModel
from datetime import date
from typing import Optional


class ExtractoMovimientoBase(BaseModel):
    extracto_id: int
    cuenta_bancaria_id: int
    fecha_movimiento: date
    descripcion: Optional[str] = None
    referencia: Optional[str] = None
    monto: float
    tipo: str
    saldo_resultante: Optional[float] = None
    conciliado: bool = False


class ExtractoMovimientoCrear(ExtractoMovimientoBase):
    pass


class ExtractoMovimientoActualizar(BaseModel):
    descripcion: Optional[str] = None
    referencia: Optional[str] = None
    saldo_resultante: Optional[float] = None
    conciliado: Optional[bool] = None


class ExtractoMovimiento(ExtractoMovimientoBase):
    extracto_movimiento_id: int
    empresa_id: int

    class Config:
        from_attributes = True
