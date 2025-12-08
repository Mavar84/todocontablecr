from pydantic import BaseModel
from datetime import date
from typing import Optional


class ExtractoBancarioBase(BaseModel):
    cuenta_bancaria_id: int
    fecha_desde: date
    fecha_hasta: date
    saldo_inicial: Optional[float] = None
    saldo_final: Optional[float] = None
    archivo_url: Optional[str] = None
    observaciones: Optional[str] = None
    estado: str = "importado"


class ExtractoBancarioCrear(ExtractoBancarioBase):
    pass


class ExtractoBancarioActualizar(BaseModel):
    saldo_inicial: Optional[float] = None
    saldo_final: Optional[float] = None
    archivo_url: Optional[str] = None
    observaciones: Optional[str] = None
    estado: Optional[str] = None


class ExtractoBancario(ExtractoBancarioBase):
    extracto_id: int
    empresa_id: int

    class Config:
        from_attributes = True
