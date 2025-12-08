from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.catalogo_cuenta import (
    CatalogoCuenta,
    CatalogoCuentaCreate,
    CatalogoCuentaUpdate,
)
from app.crud.catalogo_cuenta import (
    crear_cuenta,
    listar_cuentas,
    obtener_cuenta_por_id,
    actualizar_cuenta,
    desactivar_cuenta,
)

router = APIRouter(
    prefix="/catalogo-cuentas",
    tags=["Catálogo de cuentas"],
)


@router.post("/", response_model=CatalogoCuenta, status_code=status.HTTP_201_CREATED)
def crear_catalogo_cuenta(
    cuenta_in: CatalogoCuentaCreate,
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_current_user),
):
    nueva = crear_cuenta(
        db=db,
        cuenta_in=cuenta_in,
        empresa_id=usuario_actual.empresa_id,
        usuario_id=usuario_actual.usuario_id,
    )
    return nueva


@router.get("/", response_model=list[CatalogoCuenta])
def listar_catalogo_cuentas(
    solo_activas: bool = True,
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_current_user),
):
    return listar_cuentas(
        db=db,
        empresa_id=usuario_actual.empresa_id,
        solo_activas=solo_activas,
    )


@router.get("/{cuenta_id}", response_model=CatalogoCuenta)
def obtener_catalogo_cuenta(
    cuenta_id: int,
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_current_user),
):
    cuenta = obtener_cuenta_por_id(
        db=db,
        empresa_id=usuario_actual.empresa_id,
        cuenta_id=cuenta_id,
    )
    if not cuenta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada",
        )
    return cuenta


@router.put("/{cuenta_id}", response_model=CatalogoCuenta)
def actualizar_catalogo_cuenta(
    cuenta_id: int,
    datos: CatalogoCuentaUpdate,
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_current_user),
):
    cuenta = actualizar_cuenta(
        db=db,
        empresa_id=usuario_actual.empresa_id,
        cuenta_id=cuenta_id,
        datos=datos,
        usuario_id=usuario_actual.usuario_id,
    )
    if not cuenta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada",
        )
    return cuenta


@router.delete("/{cuenta_id}", response_model=CatalogoCuenta)
def eliminar_catalogo_cuenta(
    cuenta_id: int,
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_current_user),
):
    cuenta = desactivar_cuenta(
        db=db,
        empresa_id=usuario_actual.empresa_id,
        cuenta_id=cuenta_id,
        usuario_id=usuario_actual.usuario_id,
    )
    if not cuenta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada",
        )
    return cuenta
