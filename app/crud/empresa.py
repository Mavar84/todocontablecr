from sqlalchemy.orm import Session
from app.models.empresa import Empresa
from app.schemas.empresa import EmpresaCreate

def crear_empresa(db: Session, empresa: EmpresaCreate):
    nueva = Empresa(**empresa.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def obtener_empresas(db: Session):
    return db.query(Empresa).all()

def obtener_empresa_por_id(db: Session, empresa_id: int):
    return db.query(Empresa).filter(Empresa.empresa_id == empresa_id).first()
