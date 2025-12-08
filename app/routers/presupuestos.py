from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.presupuesto import Presupuesto, PresupuestoCrear, PresupuestoActualizar
from app.crud.presupuesto import (
    crear_presupuesto,
    listar_presupuestos,
    obtener_presupuesto,
    actualizar_presupuesto,
)

router = APIRouter(prefix="/presupuestos", tags=["Presupuestos"])


@router.post("/", response_model=Presupuesto)
def crear(
    datos: PresupuestoCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_presupuesto(db, usuario.empresa_id, usuario.usuario_id, datos)


@router.get("/", response_model=list[Presupuesto])
def listar(
    anio: int | None = None,
    estado: str | None = None,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_presupuestos(db, usuario.empresa_id, anio, estado)


@router.get("/{presupuesto_id}", response_model=Presupuesto)
def obtener(
    presupuesto_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    pres = obtener_presupuesto(db, usuario.empresa_id, presupuesto_id)
    if not pres:
        raise HTTPException(404, "Presupuesto no encontrado")
    return pres


@router.put("/{presupuesto_id}", response_model=Presupuesto)
def actualizar(
    presupuesto_id: int,
    datos: PresupuestoActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    pres = actualizar_presupuesto(db, usuario.empresa_id, presupuesto_id, usuario.usuario_id, datos)
    if not pres:
        raise HTTPException(404, "Presupuesto no encontrado")
    return pres
