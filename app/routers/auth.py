# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.schemas.auth import LoginRequest, TokenResponse, SignUpRequest
from app.schemas.usuario import Usuario as UsuarioSchema, UsuarioCreate
from app.core.security import verificar_password
from app.core.jwt import crear_token, get_current_user
from app.crud.usuario import obtener_por_correo, crear_usuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Usuario comodín quemado
ADMIN_EMAIL = "admin@admin.com"
ADMIN_PASSWORD = "admin123"

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):

    # 1. Caso usuario comodín quemado
    if data.correo == ADMIN_EMAIL and data.clave == ADMIN_PASSWORD:
        # Puede ajustar el payload según lo que consuma su sistema
        token = crear_token({
            "usuario_id": 0,           # ID simbólico para admin comodín
            "correo": ADMIN_EMAIL,
            "es_admin": True
        })
        return TokenResponse(access_token=token)

    # 2. Login normal contra base de datos
    user = obtener_por_correo(db, data.correo)

    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not verificar_password(data.clave, user.clave_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = crear_token({
        "usuario_id": user.usuario_id,
        "correo": user.correo,
        "es_admin": False
    })

    return TokenResponse(access_token=token)


@router.post("/signup", response_model=UsuarioSchema)
def signup(
    data: SignUpRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)  # exige JWT válido
):
    """
    Crea un nuevo usuario en el sistema.
    Requiere estar autenticado con JWT (por ejemplo, usando el admin comodín).
    """

    # Validar que el correo no esté repetido
    existente = obtener_por_correo(db, data.correo)
    if existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # Reutilizamos UsuarioCreate del esquema de usuario
    usuario_create = UsuarioCreate(
        nombre=data.nombre,
        correo=data.correo,
        clave=data.clave
    )

    nuevo_usuario = crear_usuario(db, usuario_create, data.empresa_id)

    return nuevo_usuario
