from pydantic import BaseModel, EmailStr
from typing import Optional


class ClienteBase(BaseModel):
    nombre: str
    identificacion: Optional[str] = None
    tipo_identificacion: Optional[str] = None
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    limite_credito: Optional[float] = None
    dias_credito: Optional[int] = None
    activo: bool = True


class ClienteCrear(ClienteBase):
    pass


class ClienteActualizar(BaseModel):
    nombre: Optional[str] = None
    identificacion: Optional[str] = None
    tipo_identificacion: Optional[str] = None
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    limite_credito: Optional[float] = None
    dias_credito: Optional[int] = None
    activo: Optional[bool] = None


class Cliente(ClienteBase):
    cliente_id: int
    empresa_id: int

    class Config:
        from_attributes = True
