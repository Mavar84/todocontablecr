from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.retencion_aplicada import RetencionAplicada, RetencionAplicadaCrear
from app.crud.retencion_aplicada import aplicar_retencion

router = APIRouter(prefix="/retenciones-aplicadas", tags=["Retenciones - aplicadas"])


@router.post("/", response_model=RetencionAplicada)
def crear(
    datos: RetencionAplicadaCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        return aplicar_retencion(db, usuario.empresa_id, datos)
    except ValueError as e:
        raise HTTPException(400, str(e))
