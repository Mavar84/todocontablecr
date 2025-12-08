from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.factura_venta import FacturaVentaCreate, FacturaVenta
from app.crud.factura_venta import crear_factura, listar_facturas, obtener_factura

router = APIRouter(
    prefix="/facturas-venta",
    tags=["Facturación ventas"],
)


@router.post("/", response_model=FacturaVenta)
def crear(
    data: FacturaVentaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        return crear_factura(
            db=db,
            data=data,
            empresa_id=usuario.empresa_id,
            usuario_id=usuario.usuario_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[FacturaVenta])
def listar(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_facturas(db, usuario.empresa_id)


@router.get("/{factura_id}", response_model=FacturaVenta)
def obtener(
    factura_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    factura = obtener_factura(db, usuario.empresa_id, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura
