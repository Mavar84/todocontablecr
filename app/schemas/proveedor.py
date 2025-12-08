from pydantic import BaseModel, EmailStr
from typing import Optional


class ProveedorBase(BaseModel):
    nombre: str
    identificacion: Optional[str] = None
    tipo_identificacion: Optional[str] = None
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    limite_credito: Optional[float] = None
    dias_credito: Optional[int] = None
    activo: bool = True


class ProveedorCrear(ProveedorBase):
    pass


class ProveedorActualizar(BaseModel):
    nombre: Optional[str] = None
    identificacion: Optional[str] = None
    tipo_identificacion: Optional[str] = None
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    limite_credito: Optional[float] = None
    dias_credito: Optional[int] = None
    activo: Optional[bool] = None


class Proveedor(ProveedorBase):
    proveedor_id: int
    empresa_id: int

    class Config:
        from_attributes = True
