from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.producto_impuesto import (
    ProductoImpuesto,
    ProductoImpuestoCrear,
    ProductoImpuestoActualizar,
)
from app.crud.producto_impuesto import (
    asignar_impuesto_a_producto,
    listar_impuestos_de_producto,
    actualizar_producto_impuesto,
)

router = APIRouter(prefix="/productos-impuestos", tags=["Productos e impuestos"])


@router.post("/", response_model=ProductoImpuesto)
def asignar(
    datos: ProductoImpuestoCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return asignar_impuesto_a_producto(db, datos)


@router.get("/producto/{producto_id}", response_model=list[ProductoImpuesto])
def listar_de_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_impuestos_de_producto(db, producto_id)


@router.put("/{producto_impuesto_id}", response_model=ProductoImpuesto)
def actualizar(
    producto_impuesto_id: int,
    datos: ProductoImpuestoActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    pi = actualizar_producto_impuesto(db, producto_impuesto_id, datos)
    if not pi:
        raise HTTPException(404, "Relación producto-impuesto no encontrada")
    return pi
