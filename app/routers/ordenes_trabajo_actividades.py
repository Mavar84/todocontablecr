from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.orden_trabajo_actividad import (
    OrdenTrabajoActividad,
    OrdenTrabajoActividadCrear,
)
from app.crud.orden_trabajo_actividad import (
    crear_actividad_ot,
    listar_actividades_ot,
)

router = APIRouter(prefix="/ordenes-trabajo-actividades", tags=["Órdenes de trabajo - actividades"])


@router.post("/", response_model=OrdenTrabajoActividad)
def crear(
    datos: OrdenTrabajoActividadCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        return crear_actividad_ot(db, usuario.empresa_id, usuario.usuario_id, datos)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/por-orden/{orden_trabajo_id}", response_model=list[OrdenTrabajoActividad])
def listar(
    orden_trabajo_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_actividades_ot(db, usuario.empresa_id, orden_trabajo_id)
