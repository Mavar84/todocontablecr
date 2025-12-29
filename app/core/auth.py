from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from app.core.jwt import verificar_token
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):

    payload = verificar_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )

    # ------------------------------------------------------
    # 1. ADMIN COMODÍN: usuario virtual, no se consulta DB
    # ------------------------------------------------------
    if payload.get("usuario_id") == 0 and payload.get("es_admin") is True:
        return SimpleNamespace(
            usuario_id=0,
            nombre="Administrador",
            correo=payload.get("correo", "admin@admin.com"),
            es_admin=True
        )

    # ------------------------------------------------------
    # 2. USUARIO NORMAL → buscar en BD
    # ------------------------------------------------------
    user = db.query(Usuario).filter(Usuario.usuario_id == payload["usuario_id"]).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    return user

