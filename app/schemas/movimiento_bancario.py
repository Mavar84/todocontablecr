from pydantic import BaseModel
from datetime import date
from typing import Optional


class MovimientoBancarioBase(BaseModel):
    cuenta_bancaria_id: int
    fecha: date
    descripcion: Optional[str] = None
    monto: float
    comprobante_id: Optional[int] = None


class MovimientoBancarioCrear(MovimientoBancarioBase):
    pass


class MovimientoBancario(MovimientoBancarioBase):
    movimiento_bancario_id: int
    empresa_id: int
    conciliado: bool

    class Config:
        from_attributes = True
