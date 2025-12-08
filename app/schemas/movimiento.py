from datetime import datetime
from pydantic import BaseModel


class MovimientoBase(BaseModel):
    cuenta_id: int
    descripcion: str | None = None
    debe: float = 0
    haber: float = 0
    centro_costo_id: int | None = None
    bodega_id: int | None = None


class MovimientoCreate(MovimientoBase):
    pass


class Movimiento(MovimientoBase):
    movimiento_id: int

    class Config:
        from_attributes = True
