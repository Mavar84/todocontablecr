from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.proveedor import Proveedor, ProveedorCrear, ProveedorActualizar
from app.crud.proveedor import (
    crear_proveedor,
    listar_proveedores,
    obtener_proveedor,
    actualizar_proveedor,
)

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


@router.post("/", response_model=Proveedor)
def crear(
    datos: ProveedorCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_proveedor(db, usuario.empresa_id, usuario.usuario_id, datos)


@router.get("/", response_model=list[Proveedor])
def listar(
    solo_activos: bool = True,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_proveedores(db, usuario.empresa_id, solo_activos)


@router.get("/{proveedor_id}", response_model=Proveedor)
def obtener(
    proveedor_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    prv = obtener_proveedor(db, usuario.empresa_id, proveedor_id)
    if not prv:
        raise HTTPException(404, "Proveedor no encontrado")
    return prv


@router.put("/{proveedor_id}", response_model=Proveedor)
def actualizar(
    proveedor_id: int,
    datos: ProveedorActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    prv = actualizar_proveedor(db, usuario.empresa_id, proveedor_id, usuario.usuario_id, datos)
    if not prv:
        raise HTTPException(404, "Proveedor no encontrado")
    return prv
