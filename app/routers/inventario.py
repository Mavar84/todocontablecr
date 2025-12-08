from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.inventario import (
    MovimientoInventarioCrear,
    MovimientoInventario,
)
from app.crud.inventario import (
    registrar_movimiento,
    listar_movimientos,
)

router = APIRouter(prefix="/inventario", tags=["Inventario"])


@router.post("/movimientos", response_model=MovimientoInventario)
def crear_movimiento_inventario_endpoint(
    datos: MovimientoInventarioCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        return registrar_movimiento(db, datos, usuario.empresa_id, usuario.usuario_id)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/movimientos", response_model=list[MovimientoInventario])
def listar_movimientos_inventario_endpoint(
    producto_id: int | None = None,
    bodega_id: int | None = None,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_movimientos(db, usuario.empresa_id, producto_id, bodega_id)
