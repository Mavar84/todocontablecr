from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.caja_chica_gasto import (
    CajaChicaGasto,
    CajaChicaGastoCrear,
    CajaChicaGastoActualizar,
)
from app.crud.caja_chica_gasto import (
    crear_caja_chica_gasto,
    listar_caja_chica_gastos,
    obtener_caja_chica_gasto,
    actualizar_caja_chica_gasto,
)

router = APIRouter(prefix="/caja-chica-gastos", tags=["Caja chica - gastos"])


@router.post("/", response_model=CajaChicaGasto)
def crear(
    datos: CajaChicaGastoCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        return crear_caja_chica_gasto(db, usuario.empresa_id, usuario.usuario_id, datos)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/", response_model=list[CajaChicaGasto])
def listar(
    caja_chica_id: int | None = None,
    estado: str | None = None,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_caja_chica_gastos(db, usuario.empresa_id, caja_chica_id, estado)


@router.get("/{gasto_id}", response_model=CajaChicaGasto)
def obtener(
    gasto_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    gasto = obtener_caja_chica_gasto(db, usuario.empresa_id, gasto_id)
    if not gasto:
        raise HTTPException(404, "Gasto de caja chica no encontrado")
    return gasto


@router.put("/{gasto_id}", response_model=CajaChicaGasto)
def actualizar(
    gasto_id: int,
    datos: CajaChicaGastoActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    gasto = actualizar_caja_chica_gasto(db, usuario.empresa_id, gasto_id, usuario.usuario_id, datos)
    if not gasto:
        raise HTTPException(404, "Gasto de caja chica no encontrado")
    return gasto
