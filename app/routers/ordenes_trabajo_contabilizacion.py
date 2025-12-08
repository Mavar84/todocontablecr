from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.services.contabilizar_orden_trabajo import contabilizar_orden_trabajo

router = APIRouter(prefix="/ordenes-trabajo-contabilizacion", tags=["Órdenes de trabajo - contabilización"])


@router.post("/{orden_trabajo_id}")
def contabilizar(
    orden_trabajo_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        comprobante = contabilizar_orden_trabajo(db, usuario.empresa_id, usuario.usuario_id, orden_trabajo_id)
        return {
            "mensaje": "Orden de trabajo contabilizada correctamente",
            "comprobante_id": comprobante.comprobante_id
        }
    except ValueError as e:
        raise HTTPException(400, str(e))
