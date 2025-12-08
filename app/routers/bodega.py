from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.bodega import Bodega, BodegaCrear, BodegaActualizar
from app.crud.bodega import (
    crear_bodega,
    listar_bodegas,
    obtener_bodega,
    actualizar_bodega,
)

router = APIRouter(prefix="/bodegas", tags=["Bodegas"])


@router.post("/", response_model=Bodega)
def crear_bodega_endpoint(
    datos: BodegaCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_bodega(db, datos, usuario.empresa_id, usuario.usuario_id)


@router.get("/", response_model=list[Bodega])
def listar_bodegas_endpoint(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_bodegas(db, usuario.empresa_id)


@router.get("/{bodega_id}", response_model=Bodega)
def obtener_bodega_endpoint(
    bodega_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    bodega = obtener_bodega(db, usuario.empresa_id, bodega_id)
    if not bodega:
        raise HTTPException(404, "Bodega no encontrada")
    return bodega


@router.put("/{bodega_id}", response_model=Bodega)
def actualizar_bodega_endpoint(
    bodega_id: int,
    datos: BodegaActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    bodega = actualizar_bodega(db, usuario.empresa_id, bodega_id, datos, usuario.usuario_id)
    if not bodega:
        raise HTTPException(404, "Bodega no encontrada")
    return bodega
