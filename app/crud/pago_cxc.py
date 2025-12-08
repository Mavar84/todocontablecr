from sqlalchemy.orm import Session

from app.models.pago_cxc import PagoCXC


def listar_pagos_cxc(db: Session, empresa_id: int, cxc_id: int | None = None):
    q = db.query(PagoCXC).filter(PagoCXC.empresa_id == empresa_id)
    if cxc_id:
        q = q.filter(PagoCXC.cxc_id == cxc_id)
    return q.order_by(PagoCXC.fecha_pago.desc(), PagoCXC.pago_cxc_id.desc()).all()
