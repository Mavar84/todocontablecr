from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.orden_trabajo_material_plan import (
    OrdenTrabajoMaterialPlan,
    OrdenTrabajoMaterialPlanCrear,
    OrdenTrabajoMaterialPlanActualizar,
)
from app.crud.orden_trabajo_material_plan import (
    crear_material_plan,
    listar_materiales_plan,
    obtener_material_plan,
    actualizar_material_plan,
)

router = APIRouter(prefix="/ordenes-trabajo-material-plan", tags=["Órdenes de trabajo - materiales plan"])


@router.post("/", response_model=OrdenTrabajoMaterialPlan)
def crear(
    datos: OrdenTrabajoMaterialPlanCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        return crear_material_plan(db, usuario.empresa_id, usuario.usuario_id, datos)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/por-orden/{orden_trabajo_id}", response_model=list[OrdenTrabajoMaterialPlan])
def listar(
    orden_trabajo_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_materiales_plan(db, usuario.empresa_id, orden_trabajo_id)


@router.get("/{material_plan_id}", response_model=OrdenTrabajoMaterialPlan)
def obtener(
    material_plan_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    mat = obtener_material_plan(db, usuario.empresa_id, material_plan_id)
    if not mat:
        raise HTTPException(404, "Material plan no encontrado")
    return mat


@router.put("/{material_plan_id}", response_model=OrdenTrabajoMaterialPlan)
def actualizar(
    material_plan_id: int,
    datos: OrdenTrabajoMaterialPlanActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    mat = actualizar_material_plan(db, usuario.empresa_id, material_plan_id, usuario.usuario_id, datos)
    if not mat:
        raise HTTPException(404, "Material plan no encontrado")
    return mat
