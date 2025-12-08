from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.configuracion_fe import (
    ConfiguracionFECrear,
    ConfiguracionFEActualizar,
    ConfiguracionFE,
)
from app.crud.configuracion_fe import (
    obtener_configuracion_fe,
    crear_o_actualizar_configuracion_fe,
)

router = APIRouter(prefix="/configuracion-fe", tags=["Factura electrónica - configuración"])


@router.get("/", response_model=ConfiguracionFE)
def obtener(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    config = obtener_configuracion_fe(db, usuario.empresa_id)
    if not config:
        raise HTTPException(404, "No hay configuración de factura electrónica para esta empresa")
    return config


@router.post("/", response_model=ConfiguracionFE)
def crear_o_actualizar(
    datos: ConfiguracionFECrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_o_actualizar_configuracion_fe(db, usuario.empresa_id, usuario.usuario_id, datos)


@router.put("/", response_model=ConfiguracionFE)
def actualizar(
    datos: ConfiguracionFEActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_o_actualizar_configuracion_fe(db, usuario.empresa_id, usuario.usuario_id, datos)
