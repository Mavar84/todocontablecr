from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.caja_chica import (
    CajaChica,
    CajaChicaCrear,
    CajaChicaActualizar,
)
from app.crud.caja_chica import (
    crear_caja_chica,
    listar_cajas_chica,
    obtener_caja_chica,
    actualizar_caja_chica,
)

router = APIRouter(prefix="/caja-chica", tags=["Caja chica - cajas"])


@router.post("/", response_model=CajaChica)
def crear(
    datos: CajaChicaCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_caja_chica(db, usuario.empresa_id, usuario.usuario_id, datos)


@router.get("/", response_model=list[CajaChica])
def listar(
    solo_activas: bool = True,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_cajas_chica(db, usuario.empresa_id, solo_activas)


@router.get("/{caja_chica_id}", response_model=CajaChica)
def obtener(
    caja_chica_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    caja = obtener_caja_chica(db, usuario.empresa_id, caja_chica_id)
    if not caja:
        raise HTTPException(404, "Caja chica no encontrada")
    return caja


@router.put("/{caja_chica_id}", response_model=CajaChica)
def actualizar(
    caja_chica_id: int,
    datos: CajaChicaActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    caja = actualizar_caja_chica(db, usuario.empresa_id, caja_chica_id, usuario.usuario_id, datos)
    if not caja:
        raise HTTPException(404, "Caja chica no encontrada")
    return caja
