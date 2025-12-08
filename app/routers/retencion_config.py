from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.retencion_config import (
    RetencionConfig,
    RetencionConfigCrear,
    RetencionConfigActualizar,
)
from app.crud.retencion_config import (
    crear_retencion_config,
    listar_retenciones_config,
    obtener_retencion_config,
    actualizar_retencion_config,
)

router = APIRouter(prefix="/retenciones-config", tags=["Retenciones - configuración"])


@router.post("/", response_model=RetencionConfig)
def crear(
    datos: RetencionConfigCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_retencion_config(db, usuario.empresa_id, datos)


@router.get("/", response_model=list[RetencionConfig])
def listar(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_retenciones_config(db, usuario.empresa_id)


@router.get("/{retencion_config_id}", response_model=RetencionConfig)
def obtener(
    retencion_config_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    rc = obtener_retencion_config(db, usuario.empresa_id, retencion_config_id)
    if not rc:
        raise HTTPException(404, "Configuración de retención no encontrada")
    return rc


@router.put("/{retencion_config_id}", response_model=RetencionConfig)
def actualizar(
    retencion_config_id: int,
    datos: RetencionConfigActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    rc = actualizar_retencion_config(db, usuario.empresa_id, retencion_config_id, datos)
    if not rc:
        raise HTTPException(404, "Configuración de retención no encontrada")
    return rc
