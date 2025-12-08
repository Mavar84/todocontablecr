from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user

from app.service.contabilizar_planilla import contabilizar_planilla


router = APIRouter(prefix="/planilla-contabilizacion", tags=["Planilla - Contabilización"])


@router.post("/{planilla_id}")
def contabilizar(
    planilla_id: int,
    cuentas: dict,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    """
    cuentas = {
        "gastos_personal": 1001,
        "sueldos_por_pagar": 2001,
        "obrero_por_pagar": 2002,
        "patrono_por_pagar": 2003,
        "renta_por_pagar": 2004
    }
    """
    try:
        comprob = contabilizar_planilla(
            db=db,
            empresa_id=usuario.empresa_id,
            usuario_id=usuario.usuario_id,
            planilla_id=planilla_id,
            cuentas=cuentas
        )
        return {
            "mensaje": "Planilla contabilizada correctamente",
            "comprobante_id": comprob.comprobante_id
        }
    except ValueError as e:
        raise HTTPException(400, str(e))
