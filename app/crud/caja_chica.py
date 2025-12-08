from datetime import datetime
from sqlalchemy.orm import Session

from app.models.caja_chica import CajaChica
from app.schemas.caja_chica import CajaChicaCrear, CajaChicaActualizar


def crear_caja_chica(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    datos: CajaChicaCrear,
):
    caja = CajaChica(
        empresa_id=empresa_id,
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        moneda_id=datos.moneda_id,
        monto_maximo=datos.monto_maximo,
        saldo_inicial=datos.saldo_inicial,
        saldo_actual=datos.saldo_actual,
        cuenta_contable_id=datos.cuenta_contable_id,
        responsable_usuario_id=datos.responsable_usuario_id,
        activa=datos.activa,
        creado_por=usuario_id,
        creado_en=datetime.utcnow(),
    )
    db.add(caja)
    db.commit()
    db.refresh(caja)
    return caja


def listar_cajas_chica(
    db: Session,
    empresa_id: int,
    solo_activas: bool = True,
):
    q = db.query(CajaChica).filter(CajaChica.empresa_id == empresa_id)
    if solo_activas:
        q = q.filter(CajaChica.activa == True)
    return q.order_by(CajaChica.nombre).all()


def obtener_caja_chica(
    db: Session,
    empresa_id: int,
    caja_chica_id: int,
):
    return (
        db.query(CajaChica)
        .filter(
            CajaChica.empresa_id == empresa_id,
            CajaChica.caja_chica_id == caja_chica_id,
        )
        .first()
    )


def actualizar_caja_chica(
    db: Session,
    empresa_id: int,
    caja_chica_id: int,
    usuario_id: int,
    datos: CajaChicaActualizar,
):
    caja = obtener_caja_chica(db, empresa_id, caja_chica_id)
    if not caja:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(caja, campo, valor)

    caja.actualizado_por = usuario_id
    caja.actualizado_en = datetime.utcnow()

    db.commit()
    db.refresh(caja)
    return caja
