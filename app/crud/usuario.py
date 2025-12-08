from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.core.security import hash_password

def crear_usuario(db: Session, usuario: UsuarioCreate, empresa_id: int):
    nuevo = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        clave_hash=hash_password(usuario.clave),
        empresa_id=empresa_id,
        activo=True
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_por_correo(db: Session, correo: str):
    return db.query(Usuario).filter(Usuario.correo == correo).first()
