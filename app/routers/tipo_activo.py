from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.tipo_activo import TipoActivoCrear, TipoActivoActualizar, TipoActivo
from app.crud.tipo_activo import (
    crear_tipo_activo,
    listar_tipos_activo,
    obtener_tipo_activo,
    actualizar_tipo_activo,
)

router = APIRouter(prefix="/tipos-activo", tags=["Tipos de Activo"])


@router.post("/", response_model=TipoActivo)
def crear(data: TipoActivoCrear, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    return crear_tipo_activo(db, data, usuario.empresa_id, usuario.usuario_id)


@router.get("/", response_model=list[TipoActivo])
def listar(db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    return listar_tipos_activo(db, usuario.empresa_id)


@router.get("/{tipo_activo_id}", response_model=TipoActivo)
def obtener(tipo_activo_id: int, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    tipo = obtener_tipo_activo(db, usuario.empresa_id, tipo_activo_id)
    if not tipo:
        raise HTTPException(404, "Tipo de activo no encontrado")
    return tipo


@router.put("/{tipo_activo_id}", response_model=TipoActivo)
def actualizar(tipo_activo_id: int, datos: TipoActivoActualizar, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    tipo = actualizar_tipo_activo(db, usuario.empresa_id, tipo_activo_id, datos)
    if not tipo:
        raise HTTPException(404, "Tipo de activo no encontrado")
    return tipo
