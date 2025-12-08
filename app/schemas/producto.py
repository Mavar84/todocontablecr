from pydantic import BaseModel
from typing import Optional


class ProductoBase(BaseModel):
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    unidad_medida: Optional[str] = None
    cabys: Optional[str] = None
    es_inventariable: bool = True
    activo: bool = True
    cuenta_inventario_id: Optional[int] = None
    cuenta_costo_venta_id: Optional[int] = None
    cuenta_ingreso_id: Optional[int] = None


class ProductoCrear(ProductoBase):
    pass


class ProductoActualizar(BaseModel):
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    unidad_medida: Optional[str] = None
    cabys: Optional[str] = None
    es_inventariable: Optional[bool] = None
    activo: Optional[bool] = None
    cuenta_inventario_id: Optional[int] = None
    cuenta_costo_venta_id: Optional[int] = None
    cuenta_ingreso_id: Optional[int] = None


class Producto(ProductoBase):
    producto_id: int
    empresa_id: int

    class Config:
        from_attributes = True
