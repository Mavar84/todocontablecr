from decimal import Decimal
from sqlalchemy.orm import Session
from datetime import date

from app.crud.orden_trabajo import obtener_orden_trabajo, recalcular_costos_orden_trabajo
from app.models.orden_trabajo_consumo_material import OrdenTrabajoConsumoMaterial
from app.models.orden_trabajo_actividad import OrdenTrabajoActividad
from app.models.config_contable_produccion import ConfigContableProduccion

from app.crud.comprobante import crear_comprobante_automatico


def contabilizar_orden_trabajo(db: Session, empresa_id: int, usuario_id: int, orden_trabajo_id: int):
    ot = obtener_orden_trabajo(db, empresa_id, orden_trabajo_id)
    if not ot:
        raise ValueError("Orden de trabajo no encontrada")

    # actualizar costos
    ot = recalcular_costos_orden_trabajo(db, empresa_id, orden_trabajo_id)

    config = (
        db.query(ConfigContableProduccion)
        .filter(ConfigContableProduccion.empresa_id == empresa_id)
        .first()
    )
    if not config:
        raise ValueError("Debe configurar las cuentas contables de producción")

    # CONTABILIZACIÓN
    asientos = []

    # 1. Materiales → DB PIP, CR Inventario
    if ot.costo_materiales > 0:
        asientos.append({
            "cuenta_id": config.cuenta_pip_id,
            "debe": float(ot.costo_materiales),
            "haber": 0,
            "detalle": "Materiales consumidos OT " + ot.codigo,
        })
        asientos.append({
            "cuenta_id": config.cuenta_mp_id,
            "debe": 0,
            "haber": float(ot.costo_materiales),
            "detalle": "Salida MP OT " + ot.codigo,
        })

    # 2. Mano de obra directa → DB PIP, CR MO aplicada
    if ot.costo_mano_obra > 0:
        asientos.append({
            "cuenta_id": config.cuenta_pip_id,
            "debe": float(ot.costo_mano_obra),
            "haber": 0,
            "detalle": "Mano de obra directa OT " + ot.codigo,
        })
        asientos.append({
            "cuenta_id": config.cuenta_mo_id,
            "debe": 0,
            "haber": float(ot.costo_mano_obra),
            "detalle": "MO aplicada OT " + ot.codigo,
        })

    # 3. Costos indirectos → DB PIP, CR CIF asignado
    if ot.costo_indirectos > 0:
        asientos.append({
            "cuenta_id": config.cuenta_pip_id,
            "debe": float(ot.costo_indirectos),
            "haber": 0,
            "detalle": "Costos indirectos OT " + ot.codigo,
        })
        asientos.append({
            "cuenta_id": config.cuenta_cif_id,
            "debe": 0,
            "haber": float(ot.costo_indirectos),
            "detalle": "CIF asignados OT " + ot.codigo,
        })

    # 4. Paso del PIP → Producto terminado
    if ot.costo_total > 0:
        asientos.append({
            "cuenta_id": config.cuenta_pt_id,
            "debe": float(ot.costo_total),
            "haber": 0,
            "detalle": "Ingreso a PT desde OT " + ot.codigo,
        })
        asientos.append({
            "cuenta_id": config.cuenta_pip_id,
            "debe": 0,
            "haber": float(ot.costo_total),
            "detalle": "Salida PIP por OT " + ot.codigo,
        })

    # =======================
    # CREAR COMPROBANTE
    # =======================
    comprobante = crear_comprobante_automatico(
        db=db,
        empresa_id=empresa_id,
        usuario_id=usuario_id,
        fecha=date.today(),
        descripcion=f"Contabilización automática de OT {ot.codigo}",
        lineas=asientos,
        tipo="OT",
        referencia_id=orden_trabajo_id
    )

    # cambiar estado de la OT a finalizada/cerrada
    ot.estado = "cerrada"
    db.commit()

    return comprobante
