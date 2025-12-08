from pydantic import BaseModel
from typing import Optional


class MonedaBase(BaseModel):
    codigo: str
    nombre: str
    simbolo: Optional[str] = None
    es_base: bool = False
    decimales: int = 2


class MonedaCrear(MonedaBase):
    pass


class MonedaActualizar(BaseModel):
    nombre: Optional[str] = None
    simbolo: Optional[str] = None
    es_base: Optional[bool] = None
    decimales: Optional[int] = None


class Moneda(MonedaBase):
    moneda_id: int

    class Config:
        from_attributes = True
