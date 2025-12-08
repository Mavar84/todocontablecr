from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from database import get_db
from app.core.auth import get_current_user
from app.schemas.activo_fijo import ActivoFijoCrear, ActivoFijoActualizar, ActivoFijo
from app.crud.activo_fijo import (
    crear_activo_fijo,
    listar_activos,
    obtener_activo,
    actualizar_activo,
)
from app.crud.depreciacion_activo import generar_depreciacion

router = APIRouter(prefix="/activos-fijos", tags=["Activos Fijos"])


@router.post("/", response_model=ActivoFijo)
def crear(data: ActivoFijoCrear, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    return crear_activo_fijo(db, data, usuario.empresa_id, usuario.usuario_id)


@router.get("/", response_model=list[ActivoFijo])
def listar(db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    return listar_activos(db, usuario.empresa_id)


@router.get("/{activo_id}", response_model=ActivoFijo)
def obtener_endpoint(activo_id: int, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    activo = obtener_activo(db, usuario.empresa_id, activo_id)
    if not activo:
        raise HTTPException(404, "Activo no encontrado")
    return activo


@router.put("/{activo_id}", response_model=ActivoFijo)
def actualizar_endpoint(activo_id: int, datos: ActivoFijoActualizar, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    activo = actualizar_activo(db, usuario.empresa_id, activo_id, datos, usuario.usuario_id)
    if not activo:
        raise HTTPException(404, "Activo no encontrado")
    return activo


@router.post("/{activo_id}/depreciar")
def depreciar(activo_id: int, fecha: date, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    dep = generar_depreciacion(db, activo_id, usuario.empresa_id, fecha, usuario.usuario_id)
    if not dep:
        raise HTTPException(404, "Activo no encontrado")
    return {"mensaje": "Depreciación generada", "monto": dep.monto}
