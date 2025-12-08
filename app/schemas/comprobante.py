from datetime import date, datetime
from pydantic import BaseModel
from app.schemas.movimiento import MovimientoCreate, Movimiento


class ComprobanteBase(BaseModel):
    fecha: date
    descripcion: str | None = None
    tipo_comprobante_id: int | None = None
    moneda_id: int | None = None
    tipo_cambio_usado: float | None = None


class ComprobanteCreate(ComprobanteBase):
    movimientos: list[MovimientoCreate]


class Comprobante(ComprobanteBase):
    comprobante_id: int
    empresa_id: int
    movimientos: list[Movimiento]

    class Config:
        from_attributes = True
