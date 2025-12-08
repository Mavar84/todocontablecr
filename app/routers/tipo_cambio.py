from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.tipo_cambio import TipoCambio, TipoCambioCrear
from app.crud.tipo_cambio import crear_tipo_cambio, listar_tipos_cambio

router = APIRouter(prefix="/tipos-cambio", tags=["Tipos de cambio"])


@router.post("/", response_model=TipoCambio)
def crear(
    datos: TipoCambioCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        return crear_tipo_cambio(db, datos)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/{moneda_id}", response_model=list[TipoCambio])
def listar(
    moneda_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_tipos_cambio(db, moneda_id)
