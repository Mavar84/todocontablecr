from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.recepcion_electronica import (
    RecepcionElectronicaCrear,
    RecepcionElectronicaActualizar,
    RecepcionElectronica,
)
from app.crud.recepcion_electronica import (
    crear_recepcion_electronica,
    obtener_recepcion,
    actualizar_recepcion,
)

router = APIRouter(prefix="/recepcion-electronica", tags=["Factura electrónica - recepción"])


@router.post("/", response_model=RecepcionElectronica)
def registrar_recepcion(
    datos: RecepcionElectronicaCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_recepcion_electronica(db, usuario.empresa_id, usuario.usuario_id, datos)


@router.get("/{recepcion_id}", response_model=RecepcionElectronica)
def obtener(
    recepcion_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    rec = obtener_recepcion(db, usuario.empresa_id, recepcion_id)
    if not rec:
        raise HTTPException(404, "Registro de recepción no encontrado")
    return rec


@router.put("/{recepcion_id}", response_model=RecepcionElectronica)
def actualizar(
    recepcion_id: int,
    datos: RecepcionElectronicaActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    rec = actualizar_recepcion(db, usuario.empresa_id, recepcion_id, usuario.usuario_id, datos)
    if not rec:
        raise HTTPException(404, "Registro de recepción no encontrado")
    return rec
