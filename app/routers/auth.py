from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import verificar_password
from app.core.jwt import crear_token
from app.crud.usuario import obtener_por_correo

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = obtener_por_correo(db, data.correo)

    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not verificar_password(data.clave, user.clave_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = crear_token({"usuario_id": user.usuario_id})

    return TokenResponse(access_token=token)
