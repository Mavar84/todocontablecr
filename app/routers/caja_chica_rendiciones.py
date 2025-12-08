from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.caja_chica_rendicion import (
    CajaChicaRendicion,
    CajaChicaRendicionCrear,
    CajaChicaRendicionActualizar,
)
from app.schemas.caja_chica_rendicion_asignacion import CajaChicaRendicionAsignacion
from app.crud.caja_chica_rendicion import (
    crear_caja_chica_rendicion,
    listar_caja_chica_rendiciones,
    obtener_caja_chica_rendicion,
    actualizar_caja_chica_rendicion,
    asignar_gastos_a_rendicion,
)

router = APIRouter(prefix="/caja-chica-rendiciones", tags=["Caja chica - rendiciones"])


@router.post("/", response_model=CajaChicaRendicion)
def crear(
    datos: CajaChicaRendicionCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return crear_caja_chica_rendicion(db, usuario.empresa_id, usuario.usuario_id, datos)


@router.get("/", response_model=list[CajaChicaRendicion])
def listar(
    caja_chica_id: int | None = None,
    estado: str | None = None,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_caja_chica_rendiciones(db, usuario.empresa_id, caja_chica_id, estado)


@router.get("/{rendicion_id}", response_model=CajaChicaRendicion)
def obtener(
    rendicion_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    rend = obtener_caja_chica_rendicion(db, usuario.empresa_id, rendicion_id)
    if not rend:
        raise HTTPException(404, "Rendición de caja chica no encontrada")
    return rend


@router.put("/{rendicion_id}", response_model=CajaChicaRendicion)
def actualizar(
    rendicion_id: int,
    datos: CajaChicaRendicionActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    rend = actualizar_caja_chica_rendicion(db, usuario.empresa_id, rendicion_id, usuario.usuario_id, datos)
    if not rend:
        raise HTTPException(404, "Rendición de caja chica no encontrada")
    return rend


@router.post("/asignar-gastos", response_model=CajaChicaRendicion)
def asignar_gastos(
    datos: CajaChicaRendicionAsignacion,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        return asignar_gastos_a_rendicion(db, usuario.empresa_id, usuario.usuario_id, datos)
    except ValueError as e:
        raise HTTPException(400, str(e))
