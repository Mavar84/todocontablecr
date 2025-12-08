from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.orden_trabajo import (
    OrdenTrabajo,
    OrdenTrabajoCrear,
    OrdenTrabajoActualizar,
)
from app.crud.orden_trabajo import (
    crear_orden_trabajo,
    listar_ordenes_trabajo,
    obtener_orden_trabajo,
    actualizar_orden_trabajo,
    recalcular_costos_orden_trabajo,
)

router = APIRouter(prefix="/ordenes-trabajo", tags=["Órdenes de trabajo"])


@router.post("/", response_model=OrdenTrabajo)
def crear(
    datos: OrdenTrabajoCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_orden_trabajo(db, usuario.empresa_id, usuario.usuario_id, datos)


@router.get("/", response_model=list[OrdenTrabajo])
def listar(
    estado: str | None = None,
    producto_final_id: int | None = None,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_ordenes_trabajo(db, usuario.empresa_id, estado, producto_final_id)


@router.get("/{orden_trabajo_id}", response_model=OrdenTrabajo)
def obtener(
    orden_trabajo_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    ot = obtener_orden_trabajo(db, usuario.empresa_id, orden_trabajo_id)
    if not ot:
        raise HTTPException(404, "Orden de trabajo no encontrada")
    return ot


@router.put("/{orden_trabajo_id}", response_model=OrdenTrabajo)
def actualizar(
    orden_trabajo_id: int,
    datos: OrdenTrabajoActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    ot = actualizar_orden_trabajo(db, usuario.empresa_id, orden_trabajo_id, usuario.usuario_id, datos)
    if not ot:
        raise HTTPException(404, "Orden de trabajo no encontrada")
    return ot


@router.post("/{orden_trabajo_id}/recalcular-costos", response_model=OrdenTrabajo)
def recalcular_costos(
    orden_trabajo_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        return recalcular_costos_orden_trabajo(db, usuario.empresa_id, orden_trabajo_id)
    except ValueError as e:
        raise HTTPException(404, str(e))
