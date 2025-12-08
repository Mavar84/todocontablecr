from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.revaluacion_cambiaria import RevaluacionCambiaria, RevaluacionCambiariaCrear
from app.crud.revaluacion_cambiaria import generar_revaluacion_cambiaria, listar_revaluaciones, obtener_revaluacion

router = APIRouter(prefix="/revaluaciones-cambiarias", tags=["Revaluación cambiaria"])


@router.post("/", response_model=RevaluacionCambiaria)
def generar(
    datos: RevaluacionCambiariaCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        return generar_revaluacion_cambiaria(db, datos, usuario.empresa_id, usuario.usuario_id)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/", response_model=list[RevaluacionCambiaria])
def listar(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_revaluaciones(db, usuario.empresa_id)


@router.get("/{revaluacion_id}", response_model=RevaluacionCambiaria)
def obtener(
    revaluacion_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    rev = obtener_revaluacion(db, usuario.empresa_id, revaluacion_id)
    if not rev:
        raise HTTPException(404, "Revaluación no encontrada")
    return rev
