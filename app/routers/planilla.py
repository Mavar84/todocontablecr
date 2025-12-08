from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from app.core.auth import get_current_user

from app.models.planilla import Planilla
from app.schemas.planilla import (
    PlanillaCrear,
    PlanillaOut
)
from app.service.calculo_planilla import calcular_planilla


router = APIRouter(prefix="/planilla", tags=["Planilla - Generación"])


@router.post("/", response_model=PlanillaOut)
def crear_planilla(
    datos: PlanillaCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    planilla = Planilla(
        empresa_id=usuario.empresa_id,
        periodo=datos.periodo,
        fecha_pago=datos.fecha_pago,
        estado="borrador",
        creado_en=datetime.utcnow(),
    )
    db.add(planilla)
    db.commit()
    db.refresh(planilla)
    return planilla


@router.get("/", response_model=list[PlanillaOut])
def listar_planillas(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return db.query(Planilla).filter(
        Planilla.empresa_id == usuario.empresa_id
    ).order_by(Planilla.fecha_pago.desc()).all()


@router.post("/{planilla_id}/calcular", response_model=PlanillaOut)
def calcular(
    planilla_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    planilla = db.query(Planilla).filter(
        Planilla.empresa_id == usuario.empresa_id,
        Planilla.planilla_id == planilla_id
    ).first()

    if not planilla:
        raise HTTPException(404, "Planilla no encontrada")

    return calcular_planilla(db, usuario.empresa_id, planilla)
