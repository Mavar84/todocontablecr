from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.presupuesto_linea import (
    PresupuestoLinea,
    PresupuestoLineaCrear,
    PresupuestoLineaActualizar,
)
from app.crud.presupuesto_linea import (
    crear_presupuesto_linea,
    listar_presupuesto_lineas,
    obtener_presupuesto_linea,
    actualizar_presupuesto_linea,
)

router = APIRouter(prefix="/presupuestos-lineas", tags=["Presupuestos - líneas"])


@router.post("/", response_model=PresupuestoLinea)
def crear(
    datos: PresupuestoLineaCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        return crear_presupuesto_linea(db, usuario.empresa_id, usuario.usuario_id, datos)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/por-presupuesto/{presupuesto_id}", response_model=list[PresupuestoLinea])
def listar(
    presupuesto_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_presupuesto_lineas(db, usuario.empresa_id, presupuesto_id)


@router.get("/{linea_id}", response_model=PresupuestoLinea)
def obtener(
    linea_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    linea = obtener_presupuesto_linea(db, usuario.empresa_id, linea_id)
    if not linea:
        raise HTTPException(404, "Línea de presupuesto no encontrada")
    return linea


@router.put("/{linea_id}", response_model=PresupuestoLinea)
def actualizar(
    linea_id: int,
    datos: PresupuestoLineaActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    linea = actualizar_presupuesto_linea(db, usuario.empresa_id, linea_id, usuario.usuario_id, datos)
    if not linea:
        raise HTTPException(404, "Línea de presupuesto no encontrada")
    return linea
