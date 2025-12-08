from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.producto import Producto, ProductoCrear, ProductoActualizar
from app.crud.producto import (
    crear_producto,
    listar_productos,
    obtener_producto,
    actualizar_producto,
)

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/", response_model=Producto)
def crear_producto_endpoint(
    datos: ProductoCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_producto(db, datos, usuario.empresa_id, usuario.usuario_id)


@router.get("/", response_model=list[Producto])
def listar_productos_endpoint(
    solo_activos: bool = True,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_productos(db, usuario.empresa_id, solo_activos)


@router.get("/{producto_id}", response_model=Producto)
def obtener_producto_endpoint(
    producto_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    producto = obtener_producto(db, usuario.empresa_id, producto_id)
    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    return producto


@router.put("/{producto_id}", response_model=Producto)
def actualizar_producto_endpoint(
    producto_id: int,
    datos: ProductoActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    producto = actualizar_producto(db, usuario.empresa_id, producto_id, datos, usuario.usuario_id)
    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    return producto
