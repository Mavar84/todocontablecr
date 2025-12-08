from sqlalchemy.orm import Session

from app.models.pago_cxp import PagoCXP


def listar_pagos_cxp(db: Session, empresa_id: int, cxp_id: int | None = None):
    q = db.query(PagoCXP).filter(PagoCXP.empresa_id == empresa_id)
    if cxp_id:
        q = q.filter(PagoCXP.cxp_id == cxp_id)
    return q.order_by(PagoCXP.fecha_pago.desc(), PagoCXP.pago_cxp_id.desc()).all()
