from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.orden_compra import OrdenCompraCreate, OrdenCompra
from app.crud.orden_compra import (
    crear_orden_compra,
    listar_ordenes_compra,
    obtener_orden_compra,
)

router = APIRouter(
    prefix="/ordenes-compra",
    tags=["Órdenes de compra"],
)


@router.post("/", response_model=OrdenCompra)
def crear(
    data: OrdenCompraCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        return crear_orden_compra(
            db=db,
            data=data,
            empresa_id=usuario.empresa_id,
            usuario_id=usuario.usuario_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[OrdenCompra])
def listar(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_ordenes_compra(db, usuario.empresa_id)


@router.get("/{orden_compra_id}", response_model=OrdenCompra)
def obtener(
    orden_compra_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    oc = obtener_orden_compra(db, usuario.empresa_id, orden_compra_id)
    if not oc:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
    return oc
