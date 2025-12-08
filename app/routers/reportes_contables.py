from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from database import get_db
from app.core.auth import get_current_user
from app.schemas.reportes_contables import (
    BalanceComprobacionResponse,
    EstadoResultadosResponse,
    BalanceGeneralResponse,
)
from app.crud.reportes_contables import (
    obtener_balance_comprobacion,
    obtener_estado_resultados,
    obtener_balance_general,
)

router = APIRouter(prefix="/reportes", tags=["Reportes contables"])


@router.get("/balance-comprobacion", response_model=BalanceComprobacionResponse)
def balance_comprobacion(
    fecha_desde: date,
    fecha_hasta: date,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    if fecha_desde > fecha_hasta:
        raise HTTPException(400, "La fecha_desde no puede ser mayor que fecha_hasta")

    return obtener_balance_comprobacion(
        db=db,
        empresa_id=usuario.empresa_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
    )


@router.get("/estado-resultados", response_model=EstadoResultadosResponse)
def estado_resultados(
    fecha_desde: date,
    fecha_hasta: date,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    if fecha_desde > fecha_hasta:
        raise HTTPException(400, "La fecha_desde no puede ser mayor que fecha_hasta")

    return obtener_estado_resultados(
        db=db,
        empresa_id=usuario.empresa_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
    )


@router.get("/balance-general", response_model=BalanceGeneralResponse)
def balance_general(
    fecha_desde: date,
    fecha_hasta: date,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    if fecha_desde > fecha_hasta:
        raise HTTPException(400, "La fecha_desde no puede ser mayor que fecha_hasta")

    return obtener_balance_general(
        db=db,
        empresa_id=usuario.empresa_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
    )
