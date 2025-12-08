from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.caja_chica import CajaChica
from app.models.caja_chica_gasto import CajaChicaGasto
from app.schemas.caja_chica_gasto import CajaChicaGastoCrear, CajaChicaGastoActualizar


def crear_caja_chica_gasto(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    datos: CajaChicaGastoCrear,
):
    caja = (
        db.query(CajaChica)
        .filter(
            CajaChica.empresa_id == empresa_id,
            CajaChica.caja_chica_id == datos.caja_chica_id,
        )
        .first()
    )
    if not caja:
        raise ValueError("Caja chica no encontrada para esta empresa")

    saldo_actual = Decimal(str(caja.saldo_actual))
    monto = Decimal(str(datos.monto))

    if monto <= 0:
        raise ValueError("El monto del gasto debe ser mayor a cero")

    if saldo_actual < monto:
        raise ValueError("No hay saldo suficiente en la caja chica")

    gasto = CajaChicaGasto(
        empresa_id=empresa_id,
        caja_chica_id=datos.caja_chica_id,
        fecha=datos.fecha,
        descripcion=datos.descripcion,
        proveedor=datos.proveedor,
        comprobante_numero=datos.comprobante_numero,
        monto=monto,
        moneda_id=datos.moneda_id,
        cuenta_contable_id=datos.cuenta_contable_id,
        centro_costo_id=datos.centro_costo_id,
        estado="registrado",
        documento_url=datos.documento_url,
        creado_por=usuario_id,
        creado_en=datetime.utcnow(),
    )
    db.add(gasto)

    caja.saldo_actual = saldo_actual - monto
    caja.actualizado_por = usuario_id
    caja.actualizado_en = datetime.utcnow()

    db.commit()
    db.refresh(gasto)
    db.refresh(caja)
    return gasto


def listar_caja_chica_gastos(
    db: Session,
    empresa_id: int,
    caja_chica_id: int | None = None,
    estado: str | None = None,
):
    q = db.query(CajaChicaGasto).filter(CajaChicaGasto.empresa_id == empresa_id)
    if caja_chica_id:
        q = q.filter(CajaChicaGasto.caja_chica_id == caja_chica_id)
    if estado:
        q = q.filter(CajaChicaGasto.estado == estado)
    return q.order_by(CajaChicaGasto.fecha.desc(), CajaChicaGasto.gasto_id.desc()).all()


def obtener_caja_chica_gasto(
    db: Session,
    empresa_id: int,
    gasto_id: int,
):
    return (
        db.query(CajaChicaGasto)
        .filter(
            CajaChicaGasto.empresa_id == empresa_id,
            CajaChicaGasto.gasto_id == gasto_id,
        )
        .first()
    )


def actualizar_caja_chica_gasto(
    db: Session,
    empresa_id: int,
    gasto_id: int,
    usuario_id: int,
    datos: CajaChicaGastoActualizar,
):
    gasto = obtener_caja_chica_gasto(db, empresa_id, gasto_id)
    if not gasto:
        return None

    cambios = datos.model_dump(exclude_unset=True)

    # no tocamos monto ni caja_chica_id ni fecha
    for campo, valor in cambios.items():
        setattr(gasto, campo, valor)

    gasto.actualizado_por = usuario_id
    gasto.actualizado_en = datetime.utcnow()

    db.commit()
    db.refresh(gasto)
    return gasto
