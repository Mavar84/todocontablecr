from pydantic import BaseModel
from typing import Optional


class CabysCodigoBase(BaseModel):
    codigo: str
    descripcion: str
    activo: bool = True


class CabysCodigoCrear(CabysCodigoBase):
    pass


class CabysCodigoActualizar(BaseModel):
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class CabysCodigo(CabysCodigoBase):
    cabys_id: int

    class Config:
        from_attributes = True
