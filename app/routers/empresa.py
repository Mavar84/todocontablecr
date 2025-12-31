from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from app.core.auth import get_current_user
from app.schemas.empresa import Empresa, EmpresaCreate
from app.crud.empresa import crear_empresa, obtener_empresas

router = APIRouter(prefix="/empresas", tags=["Empresa"])

@router.post("/", response_model=Empresa)
def crear(empresa: EmpresaCreate,
          db: Session = Depends(get_db),
          #usuario_actual = Depends(get_current_user)):
    return crear_empresa(db, empresa)

@router.get("/", response_model=list[Empresa])
def listar(db: Session = Depends(get_db),
           #usuario_actual = Depends(get_current_user)):
    return obtener_empresas(db)
