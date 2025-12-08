# app/schemas/auth.py
from pydantic import BaseModel, EmailStr

from app.schemas.usuario import UsuarioBase  # nombre, correo

class LoginRequest(BaseModel):
    correo: EmailStr
    clave: str

class SignUpRequest(UsuarioBase):
    clave: str
    empresa_id: int

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
