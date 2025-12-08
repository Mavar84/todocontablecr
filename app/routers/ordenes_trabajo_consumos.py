from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.orden_trabajo_consumo_material import (
    OrdenTrabajoConsumoMaterial,
    OrdenTrabajoConsumoMaterialCrear,
)
from app.crud.orden_trabajo_consumo_material import (
    crear_consumo_material,
    listar_consumos_material,
)

router = APIRouter(prefix="/ordenes-trabajo-consumos", tags=["Órdenes de trabajo - consumos material"])


@router.post("/", response_model=OrdenTrabajoConsumoMaterial)
def crear(
    datos: OrdenTrabajoConsumoMaterialCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        return crear_consumo_material(db, usuario.empresa_id, usuario.usuario_id, datos)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/por-orden/{orden_trabajo_id}", response_model=list[OrdenTrabajoConsumoMaterial])
def listar(
    orden_trabajo_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_consumos_material(db, usuario.empresa_id, orden_trabajo_id)
