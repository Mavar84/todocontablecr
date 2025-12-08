from datetime import datetime
from pydantic import BaseModel


class CatalogoCuentaBase(BaseModel):
    codigo: str
    nombre: str
    naturaleza: str | None = None       # "activo", "pasivo", etc.
    tipo_saldo: str | None = None
    nivel: int | None = None
    es_imputable: bool = True
    cuenta_padre_id: int | None = None
    es_depreciable: bool = False
    es_inventario: bool = False
    es_costo: bool = False
    activo: bool = True


class CatalogoCuentaCreate(CatalogoCuentaBase):
    pass


class CatalogoCuentaUpdate(BaseModel):
    codigo: str | None = None
    nombre: str | None = None
    naturaleza: str | None = None
    tipo_saldo: str | None = None
    nivel: int | None = None
    es_imputable: bool | None = None
    cuenta_padre_id: int | None = None
    es_depreciable: bool | None = None
    es_inventario: bool | None = None
    es_costo: bool | None = None
    activo: bool | None = None


class CatalogoCuenta(CatalogoCuentaBase):
    cuenta_id: int
    empresa_id: int
    created_by: int | None = None
    created_at: datetime | None = None
    updated_by: int | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
