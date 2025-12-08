from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.cuenta_cobrar import (
    CxCCreate,
    CxCMovCreate,
    CxC,
    CxCMov
)
from app.crud.cuenta_cobrar import (
    crear_cxc,
    listar_cxc,
    obtener_cxc,
    agregar_movimiento,
    actualizar_cxc,
)

router = APIRouter(prefix="/cxc", tags=["Cuentas por Cobrar"])


@router.post("/", response_model=CxC)
def crear(
    data: CxCCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return crear_cxc(db, data, usuario.empresa_id, usuario.usuario_id)


@router.get("/", response_model=list[CxC])
def listar(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return listar_cxc(db, usuario.empresa_id)


@router.get("/{cxc_id}", response_model=CxC)
def obtener(
    cxc_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    cxc = obtener_cxc(db, usuario.empresa_id, cxc_id)
    if not cxc:
        raise HTTPException(404, "Cuenta por cobrar no encontrada")
    return cxc


@router.post("/{cxc_id}/movimientos", response_model=CxCMov)
def agregar_mov(
    cxc_id: int,
    data: CxCMovCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    try:
        mov = agregar_movimiento(db, cxc_id, data, usuario.usuario_id, usuario.empresa_id)
        if not mov:
            raise HTTPException(404, "Cuenta por cobrar no encontrada")
        return mov
    except ValueError as e:
        raise HTTPException(400, str(e))
