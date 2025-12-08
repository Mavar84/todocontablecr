from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.caja_chica_rendicion import CajaChicaRendicion
from app.models.caja_chica_gasto import CajaChicaGasto
from app.models.caja_chica import CajaChica
from app.schemas.caja_chica_rendicion import (
    CajaChicaRendicionCrear,
    CajaChicaRendicionActualizar,
)
from app.schemas.caja_chica_rendicion_asignacion import CajaChicaRendicionAsignacion


def crear_caja_chica_rendicion(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    datos: CajaChicaRendicionCrear,
):
    rend = CajaChicaRendicion(
        empresa_id=empresa_id,
        caja_chica_id=datos.caja_chica_id,
        fecha_inicio=datos.fecha_inicio,
        fecha_fin=datos.fecha_fin,
        fecha_rendicion=datos.fecha_rendicion,
        estado=datos.estado,
        total_gastos=datos.total_gastos,
        total_reponer=datos.total_reponer,
        observaciones=datos.observaciones,
        comprobante_id=datos.comprobante_id,
        creado_por=usuario_id,
        creado_en=datetime.utcnow(),
    )
    db.add(rend)
    db.commit()
    db.refresh(rend)
    return rend


def listar_caja_chica_rendiciones(
    db: Session,
    empresa_id: int,
    caja_chica_id: int | None = None,
    estado: str | None = None,
):
    q = db.query(CajaChicaRendicion).filter(CajaChicaRendicion.empresa_id == empresa_id)
    if caja_chica_id:
        q = q.filter(CajaChicaRendicion.caja_chica_id == caja_chica_id)
    if estado:
        q = q.filter(CajaChicaRendicion.estado == estado)
    return q.order_by(CajaChicaRendicion.fecha_rendicion.desc()).all()


def obtener_caja_chica_rendicion(
    db: Session,
    empresa_id: int,
    rendicion_id: int,
):
    return (
        db.query(CajaChicaRendicion)
        .filter(
            CajaChicaRendicion.empresa_id == empresa_id,
            CajaChicaRendicion.rendicion_id == rendicion_id,
        )
        .first()
    )


def actualizar_caja_chica_rendicion(
    db: Session,
    empresa_id: int,
    rendicion_id: int,
    usuario_id: int,
    datos: CajaChicaRendicionActualizar,
):
    rend = obtener_caja_chica_rendicion(db, empresa_id, rendicion_id)
    if not rend:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(rend, campo, valor)

    rend.actualizado_por = usuario_id
    rend.actualizado_en = datetime.utcnow()

    db.commit()
    db.refresh(rend)
    return rend


def asignar_gastos_a_rendicion(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    datos: CajaChicaRendicionAsignacion,
):
    rend = obtener_caja_chica_rendicion(db, empresa_id, datos.rendicion_id)
    if not rend:
        raise ValueError("Rendición de caja chica no encontrada")

    gastos = (
        db.query(CajaChicaGasto)
        .filter(
            CajaChicaGasto.empresa_id == empresa_id,
            CajaChicaGasto.gasto_id.in_(datos.gastos_ids),
        )
        .all()
    )

    if not gastos:
        raise ValueError("No se encontraron gastos para asignar")

    total_gastos = Decimal("0.00")

    for g in gastos:
        if g.rendicion_id is not None and g.rendicion_id != rend.rendicion_id:
            raise ValueError(f"El gasto {g.gasto_id} ya pertenece a otra rendición")
        if g.caja_chica_id != rend.caja_chica_id:
            raise ValueError(f"El gasto {g.gasto_id} pertenece a otra caja chica")

        g.rendicion_id = rend.rendicion_id
        g.estado = "incluido_rendicion"
        g.actualizado_por = usuario_id
        g.actualizado_en = datetime.utcnow()

        total_gastos += Decimal(str(g.monto))

    rend.total_gastos = total_gastos
    rend.total_reponer = total_gastos
    rend.actualizado_por = usuario_id
    rend.actualizado_en = datetime.utcnow()

    db.commit()
    db.refresh(rend)
    return rend
