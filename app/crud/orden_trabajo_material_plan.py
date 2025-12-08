from datetime import datetime
from sqlalchemy.orm import Session

from app.models.orden_trabajo import OrdenTrabajo
from app.models.orden_trabajo_material_plan import OrdenTrabajoMaterialPlan
from app.schemas.orden_trabajo_material_plan import (
    OrdenTrabajoMaterialPlanCrear,
    OrdenTrabajoMaterialPlanActualizar,
)


def crear_material_plan(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    datos: OrdenTrabajoMaterialPlanCrear,
):
    ot = (
        db.query(OrdenTrabajo)
        .filter(
            OrdenTrabajo.empresa_id == empresa_id,
            OrdenTrabajo.orden_trabajo_id == datos.orden_trabajo_id,
        )
        .first()
    )
    if not ot:
        raise ValueError("Orden de trabajo no encontrada para esta empresa")

    mat = OrdenTrabajoMaterialPlan(
        empresa_id=empresa_id,
        orden_trabajo_id=datos.orden_trabajo_id,
        producto_id=datos.producto_id,
        bodega_id=datos.bodega_id,
        cantidad_planeada=datos.cantidad_planeada,
        unidad=datos.unidad,
        costo_unitario_estimado=datos.costo_unitario_estimado,
        costo_total_estimado=datos.costo_total_estimado,
        comentario=datos.comentario,
        creado_por=usuario_id,
        creado_en=datetime.utcnow(),
    )
    db.add(mat)
    db.commit()
    db.refresh(mat)
    return mat


def listar_materiales_plan(
    db: Session,
    empresa_id: int,
    orden_trabajo_id: int,
):
    return (
        db.query(OrdenTrabajoMaterialPlan)
        .filter(
            OrdenTrabajoMaterialPlan.empresa_id == empresa_id,
            OrdenTrabajoMaterialPlan.orden_trabajo_id == orden_trabajo_id,
        )
        .all()
    )


def obtener_material_plan(
    db: Session,
    empresa_id: int,
    material_plan_id: int,
):
    return (
        db.query(OrdenTrabajoMaterialPlan)
        .filter(
            OrdenTrabajoMaterialPlan.empresa_id == empresa_id,
            OrdenTrabajoMaterialPlan.material_plan_id == material_plan_id,
        )
        .first()
    )


def actualizar_material_plan(
    db: Session,
    empresa_id: int,
    material_plan_id: int,
    usuario_id: int,
    datos: OrdenTrabajoMaterialPlanActualizar,
):
    mat = obtener_material_plan(db, empresa_id, material_plan_id)
    if not mat:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(mat, campo, valor)

    mat.actualizado_por = usuario_id
    mat.actualizado_en = datetime.utcnow()

    db.commit()
    db.refresh(mat)
    return mat
