from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from database import get_db
from app.core.auth import get_current_user
from app.schemas.movimiento_bancario import (
    MovimientoBancario,
    MovimientoBancarioCrear,
)
from app.crud.movimiento_bancario import (
    crear_movimiento_bancario,
    listar_movimientos_bancarios,
)

router = APIRouter(prefix="/movimientos-bancarios", tags=["Movimientos bancarios"])


@router.post("/", response_model=MovimientoBancario)
def crear(
    datos: MovimientoBancarioCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_movimiento_bancario(db, datos, usuario.empresa_id, usuario.usuario_id)


@router.get("/", response_model=list[MovimientoBancario])
def listar(
    cuenta_bancaria_id: int,
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_movimientos_bancarios(
        db,
        usuario.empresa_id,
        cuenta_bancaria_id,
        fecha_desde,
        fecha_hasta,
    )
