from pydantic import BaseModel, EmailStr

class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr

class UsuarioCreate(UsuarioBase):
    clave: str

class Usuario(UsuarioBase):
    usuario_id: int
    empresa_id: int
    activo: bool

    class Config:
        from_attributes = True
