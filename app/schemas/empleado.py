from pydantic import BaseModel
from typing import Optional
from datetime import date


class EmpleadoBase(BaseModel):
    cedula: str
    nombre: str
    apellido1: str
    apellido2: Optional[str] = None
    fecha_ingreso: date
    tipo_contrato: str
    puesto: Optional[str] = None
    departamento: Optional[str] = None
    salario_base: float
    tipo_jornada: str
    centro_costo_id: Optional[int] = None


class EmpleadoCrear(EmpleadoBase):
    pass


class EmpleadoActualizar(BaseModel):
    nombre: Optional[str] = None
    apellido1: Optional[str] = None
    apellido2: Optional[str] = None
    fecha_ingreso: Optional[date] = None
    fecha_salida: Optional[date] = None
    tipo_contrato: Optional[str] = None
    puesto: Optional[str] = None
    departamento: Optional[str] = None
    salario_base: Optional[float] = None
    tipo_jornada: Optional[str] = None
    centro_costo_id: Optional[int] = None
    activo: Optional[bool] = None


class EmpleadoOut(EmpleadoBase):
    empleado_id: int
    empresa_id: int
    fecha_salida: Optional[date] = None
    activo: bool

    class Config:
        from_attributes = True
