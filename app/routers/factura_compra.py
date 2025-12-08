from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.factura_compra import FacturaCompraCreate, FacturaCompra
from app.crud.factura_compra import (
    crear_factura_compra,
    listar_facturas_compra,
    obtener_factura_compra,
)

router = APIRouter(
    prefix="/facturas-compra",
    tags=["Facturación compras"],
)


@router.post("/", response_model=FacturaCompra)
def crear(
    data: FacturaCompraCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        return crear_factura_compra(
            db=db,
            data=data,
            empresa_id=usuario.empresa_id,
            usuario_id=usuario.usuario_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[FacturaCompra])
def listar(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_facturas_compra(db, usuario.empresa_id)


@router.get("/{factura_compra_id}", response_model=FacturaCompra)
def obtener(
    factura_compra_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    fc = obtener_factura_compra(db, usuario.empresa_id, factura_compra_id)
    if not fc:
        raise HTTPException(status_code=404, detail="Factura de compra no encontrada")
    return fc
