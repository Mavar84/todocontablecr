from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.cuenta_pagar import (
    CxPCreate,
    CxPMovCreate,
    CxP,
    CxPMov,
)
from app.crud.cuenta_pagar import (
    crear_cxp,
    listar_cxp,
    obtener_cxp,
    agregar_movimiento,
    actualizar_cxp,
)

router = APIRouter(prefix="/cxp", tags=["Cuentas por Pagar"])


@router.post("/", response_model=CxP)
def crear(
    data: CxPCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return crear_cxp(db, data, usuario.empresa_id, usuario.usuario_id)


@router.get("/", response_model=list[CxP])
def listar(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return listar_cxp(db, usuario.empresa_id)


@router.get("/{cxp_id}", response_model=CxP)
def obtener(
    cxp_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    cxp = obtener_cxp(db, usuario.empresa_id, cxp_id)
    if not cxp:
        raise HTTPException(404, "Cuenta por pagar no encontrada")
    return cxp


@router.post("/{cxp_id}/movimientos", response_model=CxPMov)
def agregar_mov(
    cxp_id: int,
    data: CxPMovCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    try:
        mov = agregar_movimiento(db, cxp_id, data, usuario.usuario_id, usuario.empresa_id)
        if not mov:
            raise HTTPException(404, "Cuenta por pagar no encontrada")
        return mov
    except ValueError as e:
        raise HTTPException(400, str(e))
