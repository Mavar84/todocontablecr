from pydantic import BaseModel
from typing import Optional
from datetime import date


class OrdenTrabajoBase(BaseModel):
    codigo: str
    descripcion: Optional[str] = None
    producto_final_id: int
    cantidad_planeada: float
    cantidad_producida: Optional[float] = 0
    fecha_creacion: date
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    estado: str = "planeada"
    centro_costo_id: Optional[int] = None
    bodega_origen_id: Optional[int] = None
    bodega_destino_id: Optional[int] = None


class OrdenTrabajoCrear(OrdenTrabajoBase):
    pass


class OrdenTrabajoActualizar(BaseModel):
    descripcion: Optional[str] = None
    cantidad_planeada: Optional[float] = None
    cantidad_producida: Optional[float] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    estado: Optional[str] = None
    centro_costo_id: Optional[int] = None
    bodega_origen_id: Optional[int] = None
    bodega_destino_id: Optional[int] = None


class OrdenTrabajo(OrdenTrabajoBase):
    orden_trabajo_id: int
    empresa_id: int
    costo_materiales: float
    costo_mano_obra: float
    costo_indirectos: float
    costo_total: float
    costo_unitario: Optional[float] = None

    class Config:
        from_attributes = True
