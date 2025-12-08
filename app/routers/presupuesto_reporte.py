from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.presupuesto_reporte import ComparativoPresupuestoResponse
from app.crud.presupuesto_reporte import obtener_comparativo_presupuesto

router = APIRouter(prefix="/presupuestos-reportes", tags=["Presupuestos - reportes"])


@router.get("/comparativo/{presupuesto_id}", response_model=ComparativoPresupuestoResponse)
def comparativo(
    presupuesto_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        return obtener_comparativo_presupuesto(db, usuario.empresa_id, presupuesto_id)
    except ValueError as e:
        raise HTTPException(404, str(e))
