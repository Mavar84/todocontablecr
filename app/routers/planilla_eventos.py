from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from app.core.auth import get_current_user
from app.models.planilla_evento import PlanillaEvento
from app.schemas.planilla_evento import (
    PlanillaEventoCrear,
    PlanillaEventoOut,
)


router = APIRouter(prefix="/planilla-eventos", tags=["Planilla - Eventos"])


@router.post("/", response_model=PlanillaEventoOut)
def crear_evento(
    datos: PlanillaEventoCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    ev = PlanillaEvento(
        empleado_id=datos.empleado_id,
        empresa_id=usuario.empresa_id,
        fecha=datos.fecha,
        tipo=datos.tipo,
        cantidad=datos.cantidad,
        monto=datos.monto,
        comentario=datos.comentario,
        creado_en=datetime.utcnow(),
    )
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev


@router.get("/empleado/{empleado_id}", response_model=list[PlanillaEventoOut])
def listar_eventos_empleado(
    empleado_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    eventos = db.query(PlanillaEvento).filter(
        PlanillaEvento.empresa_id == usuario.empresa_id,
        PlanillaEvento.empleado_id == empleado_id
    ).order_by(PlanillaEvento.fecha.desc()).all()

    return eventos


@router.delete("/{evento_id}")
def eliminar_evento(
    evento_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    ev = db.query(PlanillaEvento).filter(
        PlanillaEvento.empresa_id == usuario.empresa_id,
        PlanillaEvento.evento_id == evento_id
    ).first()

    if not ev:
        raise HTTPException(404, "Evento no encontrado")

    db.delete(ev)
    db.commit()

    return {"mensaje": "Evento eliminado"}
