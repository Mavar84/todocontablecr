from pydantic import BaseModel
from typing import Optional


class ProductoImpuestoBase(BaseModel):
    producto_id: int
    impuesto_id: int
    tarifa_especifica: Optional[float] = None
    activo: bool = True


class ProductoImpuestoCrear(ProductoImpuestoBase):
    pass


class ProductoImpuestoActualizar(BaseModel):
    tarifa_especifica: Optional[float] = None
    activo: Optional[bool] = None


class ProductoImpuesto(BaseModel):
    producto_impuesto_id: int
    producto_id: int
    impuesto_id: int
    tarifa_especifica: Optional[float] = None
    activo: bool

    class Config:
        from_attributes = True
