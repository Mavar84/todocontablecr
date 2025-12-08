from pydantic import BaseModel
from datetime import date
from typing import Optional


class CertificadoFirmaBase(BaseModel):
    nombre: str
    archivo_p12_base64: str
    pin: str
    fecha_vencimiento: Optional[date] = None
    activo: bool = True


class CertificadoFirmaCrear(CertificadoFirmaBase):
    pass


class CertificadoFirmaActualizar(BaseModel):
    nombre: Optional[str] = None
    archivo_p12_base64: Optional[str] = None
    pin: Optional[str] = None
    fecha_vencimiento: Optional[date] = None
    activo: Optional[bool] = None


class CertificadoFirma(CertificadoFirmaBase):
    certificado_id: int
    empresa_id: int

    class Config:
        from_attributes = True
