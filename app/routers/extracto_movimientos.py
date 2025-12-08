from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.extracto_movimiento import (
    ExtractoMovimiento,
    ExtractoMovimientoCrear,
    ExtractoMovimientoActualizar,
)
from app.crud.extracto_movimiento import (
    crear_extracto_movimiento,
    listar_extracto_movimientos,
    obtener_extracto_movimiento,
    actualizar_extracto_movimiento,
)

router = APIRouter(prefix="/extractos-movimientos", tags=["Bancos - movimientos de extracto"])


@router.post("/", response_model=ExtractoMovimiento)
def crear(
    datos: ExtractoMovimientoCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        return crear_extracto_movimiento(db, usuario.empresa_id, datos)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/por-extracto/{extracto_id}", response_model=list[ExtractoMovimiento])
def listar(
    extracto_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_extracto_movimientos(db, usuario.empresa_id, extracto_id)


@router.get("/{extracto_movimiento_id}", response_model=ExtractoMovimiento)
def obtener(
    extracto_movimiento_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    mov = obtener_extracto_movimiento(db, usuario.empresa_id, extracto_movimiento_id)
    if not mov:
        raise HTTPException(404, "Movimiento de extracto no encontrado")
    return mov


@router.put("/{extracto_movimiento_id}", response_model=ExtractoMovimiento)
def actualizar(
    extracto_movimiento_id: int,
    datos: ExtractoMovimientoActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    mov = actualizar_extracto_movimiento(db, usuario.empresa_id, extracto_movimiento_id, datos)
    if not mov:
        raise HTTPException(404, "Movimiento de extracto no encontrado")
    return mov
