from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.impuesto import Impuesto, ImpuestoCrear, ImpuestoActualizar
from app.crud.impuesto import (
    crear_impuesto,
    listar_impuestos,
    obtener_impuesto,
    actualizar_impuesto,
)

router = APIRouter(prefix="/impuestos", tags=["Impuestos"])


@router.post("/", response_model=Impuesto)
def crear(
    datos: ImpuestoCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_impuesto(db, usuario.empresa_id, datos)


@router.get("/", response_model=list[Impuesto])
def listar(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_impuestos(db, usuario.empresa_id)


@router.get("/{impuesto_id}", response_model=Impuesto)
def obtener(
    impuesto_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    imp = obtener_impuesto(db, usuario.empresa_id, impuesto_id)
    if not imp:
        raise HTTPException(404, "Impuesto no encontrado")
    return imp


@router.put("/{impuesto_id}", response_model=Impuesto)
def actualizar(
    impuesto_id: int,
    datos: ImpuestoActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    imp = actualizar_impuesto(db, usuario.empresa_id, impuesto_id, datos)
    if not imp:
        raise HTTPException(404, "Impuesto no encontrado")
    return imp
