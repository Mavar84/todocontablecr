from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.cabys_codigo import CabysCodigo, CabysCodigoCrear, CabysCodigoActualizar
from app.crud.cabys_codigo import (
    crear_cabys,
    listar_cabys,
    obtener_cabys,
    actualizar_cabys,
)

router = APIRouter(prefix="/cabys", tags=["CABYS"])


@router.post("/", response_model=CabysCodigo)
def crear(
    datos: CabysCodigoCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_cabys(db, datos)


@router.get("/", response_model=list[CabysCodigo])
def listar(
    solo_activos: bool = True,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_cabys(db, solo_activos)


@router.get("/{cabys_id}", response_model=CabysCodigo)
def obtener(
    cabys_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    cab = obtener_cabys(db, cabys_id)
    if not cab:
        raise HTTPException(404, "Código CABYS no encontrado")
    return cab


@router.put("/{cabys_id}", response_model=CabysCodigo)
def actualizar(
    cabys_id: int,
    datos: CabysCodigoActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    cab = actualizar_cabys(db, cabys_id, datos)
    if not cab:
        raise HTTPException(404, "Código CABYS no encontrado")
    return cab
