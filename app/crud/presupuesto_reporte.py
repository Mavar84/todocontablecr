from datetime import date
from decimal import Decimal
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.presupuesto import Presupuesto
from app.models.presupuesto_linea import PresupuestoLinea
from app.models.catalogo_cuenta import CatalogoCuenta
from app.models.movimiento import Movimiento
from app.schemas.presupuesto_reporte import (
    ComparativoPresupuestoResponse,
    LineaComparativoPresupuesto,
)


def _dec(v) -> Decimal:
    if v is None:
        return Decimal("0.00")
    return Decimal(str(v))


def obtener_comparativo_presupuesto(
    db: Session,
    empresa_id: int,
    presupuesto_id: int,
) -> ComparativoPresupuestoResponse:
    pres = (
        db.query(Presupuesto)
        .filter(
            Presupuesto.empresa_id == empresa_id,
            Presupuesto.presupuesto_id == presupuesto_id,
        )
        .first()
    )
    if not pres:
        raise ValueError("Presupuesto no encontrado")

    lineas_p = (
        db.query(PresupuestoLinea, CatalogoCuenta)
        .join(
            CatalogoCuenta,
            CatalogoCuenta.cuenta_id == PresupuestoLinea.cuenta_id,
        )
        .filter(
            PresupuestoLinea.empresa_id == empresa_id,
            PresupuestoLinea.presupuesto_id == presupuesto_id,
        )
        .all()
    )

    q_ejecutado = (
        db.query(
            MovimientoContable.cuenta_id,
            extract("month", MovimientoContable.fecha).label("mes"),
            func.coalesce(func.sum(MovimientoContable.debe - MovimientoContable.haber), 0).label(
                "monto_ejecutado"
            ),
        )
        .filter(
            MovimientoContable.empresa_id == empresa_id,
            extract("year", MovimientoContable.fecha) == pres.anio,
        )
        .group_by(
            MovimientoContable.cuenta_id,
            extract("month", MovimientoContable.fecha),
        )
    )

    ejecutados_map = {}
    for row in q_ejecutado.all():
        clave = (row.cuenta_id, int(row.mes))
        ejecutados_map[clave] = _dec(row.monto_ejecutado)

    resultados: List[LineaComparativoPresupuesto] = []

    for linea, cuenta in lineas_p:
        if linea.mes is None:
            monto_ejec_acum = Decimal("0.00")
            for m in range(1, 13):
                clave = (linea.cuenta_id, m)
                monto_ejec_acum += ejecutados_map.get(clave, Decimal("0.00"))
            monto_ejecutado = monto_ejec_acum
            mes_rep = None
        else:
            clave = (linea.cuenta_id, linea.mes)
            monto_ejecutado = ejecutados_map.get(clave, Decimal("0.00"))
            mes_rep = linea.mes

        mp = _dec(linea.monto_presupuestado)
        me = monto_ejecutado
        var_abs = me - mp

        if mp == 0:
            var_pct = None
        else:
            var_pct = float((var_abs / mp) * Decimal("100.0"))

        resultados.append(
            LineaComparativoPresupuesto(
                cuenta_id=linea.cuenta_id,
                codigo_cuenta=cuenta.codigo,
                nombre_cuenta=cuenta.nombre,
                centro_costo_id=linea.centro_costo_id,
                mes=mes_rep,
                monto_presupuestado=float(mp),
                monto_ejecutado=float(me),
                variacion_absoluta=float(var_abs),
                variacion_porcentual=var_pct,
            )
        )

    return ComparativoPresupuestoResponse(
        presupuesto_id=pres.presupuesto_id,
        anio=pres.anio,
        nombre_presupuesto=pres.nombre,
        lineas=resultados,
    )
