from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    correo: EmailStr
    clave: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
