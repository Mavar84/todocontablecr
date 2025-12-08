from pydantic import BaseModel

class EmpresaBase(BaseModel):
    nombre: str
    cedula_juridica: str | None = None
    moneda_base_id: int | None = None

class EmpresaCreate(EmpresaBase):
    pass

class Empresa(EmpresaBase):
    empresa_id: int

    class Config:
        from_attributes = True
