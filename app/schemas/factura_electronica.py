from pydantic import BaseModel
from datetime import date
from typing import Optional


class FacturaElectronicaBase(BaseModel):
    factura_id: int
    tipo_documento: str
    clave: str
    consecutivo: str
    fecha_generacion: date
    xml_sin_firma: Optional[str] = None
    xml_firmado: Optional[str] = None
    xml_enviado: Optional[str] = None
    xml_respuesta: Optional[str] = None
    estado_hacienda: str = "pendiente"
    codigo_respuesta: Optional[str] = None
    mensaje_respuesta: Optional[str] = None


class FacturaElectronicaCrear(FacturaElectronicaBase):
    fecha_envio: Optional[date] = None
    fecha_respuesta: Optional[date] = None


class FacturaElectronicaActualizar(BaseModel):
    xml_firmado: Optional[str] = None
    xml_enviado: Optional[str] = None
    xml_respuesta: Optional[str] = None
    estado_hacienda: Optional[str] = None
    codigo_respuesta: Optional[str] = None
    mensaje_respuesta: Optional[str] = None
    fecha_envio: Optional[date] = None
    fecha_respuesta: Optional[date] = None


class FacturaElectronica(FacturaElectronicaBase):
    fe_id: int
    empresa_id: int
    fecha_envio: Optional[date] = None
    fecha_respuesta: Optional[date] = None

    class Config:
        from_attributes = True
