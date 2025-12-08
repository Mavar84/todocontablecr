from pydantic import BaseModel
from datetime import date
from typing import Optional


class RecepcionElectronicaBase(BaseModel):
    clave: str
    consecutivo_emisor: Optional[str] = None
    cedula_emisor: Optional[str] = None
    fecha_recepcion: date
    xml_original: str
    xml_aceptacion: Optional[str] = None
    estado_respuesta: str = "pendiente"
    mensaje_respuesta: Optional[str] = None
    factura_compra_id: Optional[int] = None


class RecepcionElectronicaCrear(RecepcionElectronicaBase):
    fecha_respuesta: Optional[date] = None


class RecepcionElectronicaActualizar(BaseModel):
    xml_aceptacion: Optional[str] = None
    estado_respuesta: Optional[str] = None
    mensaje_respuesta: Optional[str] = None
    fecha_respuesta: Optional[date] = None


class RecepcionElectronica(RecepcionElectronicaBase):
    recepcion_id: int
    empresa_id: int
    fecha_respuesta: Optional[date] = None

    class Config:
        from_attributes = True
