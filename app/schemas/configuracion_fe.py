from pydantic import BaseModel, EmailStr
from typing import Optional


class ConfiguracionFEBase(BaseModel):
    tipo_ambiente: str
    cedula_emisor: str
    nombre_comercial: Optional[str] = None
    correo_notificacion: Optional[EmailStr] = None
    sucursal: Optional[str] = None
    terminal: Optional[str] = None
    codigo_pais_telefono: Optional[str] = None
    telefono: Optional[str] = None
    usuario_api: Optional[str] = None
    clave_api: Optional[str] = None
    certificado_activo_id: Optional[int] = None
    activo: bool = True


class ConfiguracionFECrear(ConfiguracionFEBase):
    pass


class ConfiguracionFEActualizar(BaseModel):
    tipo_ambiente: Optional[str] = None
    nombre_comercial: Optional[str] = None
    correo_notificacion: Optional[EmailStr] = None
    sucursal: Optional[str] = None
    terminal: Optional[str] = None
    codigo_pais_telefono: Optional[str] = None
    telefono: Optional[str] = None
    usuario_api: Optional[str] = None
    clave_api: Optional[str] = None
    certificado_activo_id: Optional[int] = None
    activo: Optional[bool] = None


class ConfiguracionFE(ConfiguracionFEBase):
    configuracion_fe_id: int
    empresa_id: int

    class Config:
        from_attributes = True
