from pydantic import BaseModel
from typing import Optional


class BodegaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True


class BodegaCrear(BodegaBase):
    pass


class BodegaActualizar(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class Bodega(BodegaBase):
    bodega_id: int
    empresa_id: int

    class Config:
        from_attributes = True
