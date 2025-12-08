from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.cuenta_bancaria import (
    CuentaBancaria,
    CuentaBancariaCrear,
    CuentaBancariaActualizar,
)
from app.crud.cuenta_bancaria import (
    crear_cuenta_bancaria,
    listar_cuentas_bancarias,
    obtener_cuenta_bancaria,
    actualizar_cuenta_bancaria,
)

router = APIRouter(prefix="/cuentas-bancarias", tags=["Cuentas bancarias"])


@router.post("/", response_model=CuentaBancaria)
def crear(
    datos: CuentaBancariaCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_cuenta_bancaria(db, datos, usuario.empresa_id, usuario.usuario_id)


@router.get("/", response_model=list[CuentaBancaria])
def listar(
    solo_activas: bool = True,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_cuentas_bancarias(db, usuario.empresa_id, solo_activas)


@router.get("/{cuenta_bancaria_id}", response_model=CuentaBancaria)
def obtener(
    cuenta_bancaria_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    cuenta = obtener_cuenta_bancaria(db, usuario.empresa_id, cuenta_bancaria_id)
    if not cuenta:
        raise HTTPException(404, "Cuenta bancaria no encontrada")
    return cuenta


@router.put("/{cuenta_bancaria_id}", response_model=CuentaBancaria)
def actualizar(
    cuenta_bancaria_id: int,
    datos: CuentaBancariaActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    cuenta = actualizar_cuenta_bancaria(db, usuario.empresa_id, cuenta_bancaria_id, datos, usuario.usuario_id)
    if not cuenta:
        raise HTTPException(404, "Cuenta bancaria no encontrada")
    return cuenta
