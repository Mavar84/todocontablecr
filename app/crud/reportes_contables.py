from datetime import date
from decimal import Decimal
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.catalogo_cuenta import CatalogoCuenta
from app.models.movimiento import Movimiento
from app.schemas.reportes_contables import (
    BalanceComprobacionResponse,
    LineaBalanceComprobacion,
    EstadoResultadosResponse,
    LineaEstadoResultados,
    BalanceGeneralResponse,
    LineaBalanceGeneral,
)


def _dec(value) -> Decimal:
    if value is None:
        return Decimal("0.00")
    return Decimal(str(value))


def obtener_balance_comprobacion(
    db: Session,
    empresa_id: int,
    fecha_desde: date,
    fecha_hasta: date,
) -> BalanceComprobacionResponse:
    query = (
        db.query(
            CatalogoCuenta.cuenta_id,
            CatalogoCuenta.codigo,
            CatalogoCuenta.nombre,
            CatalogoCuenta.tipo,
            func.coalesce(func.sum(MovimientoContable.debe), 0).label("total_debe"),
            func.coalesce(func.sum(MovimientoContable.haber), 0).label("total_haber"),
        )
        .join(
            MovimientoContable,
            MovimientoContable.cuenta_id == CatalogoCuenta.cuenta_id,
        )
        .filter(
            CatalogoCuenta.empresa_id == empresa_id,
            MovimientoContable.empresa_id == empresa_id,
            MovimientoContable.fecha >= fecha_desde,
            MovimientoContable.fecha <= fecha_hasta,
        )
        .group_by(
            CatalogoCuenta.cuenta_id,
            CatalogoCuenta.codigo,
            CatalogoCuenta.nombre,
            CatalogoCuenta.tipo,
        )
        .order_by(CatalogoCuenta.codigo)
    )

    lineas: List[LineaBalanceComprobacion] = []
    total_debe = Decimal("0.00")
    total_haber = Decimal("0.00")
    total_saldo_deudor = Decimal("0.00")
    total_saldo_acreedor = Decimal("0.00")

    for row in query.all():
        td = _dec(row.total_debe)
        th = _dec(row.total_haber)
        saldo = td - th

        if saldo >= 0:
            saldo_deudor = saldo
            saldo_acreedor = Decimal("0.00")
        else:
            saldo_deudor = Decimal("0.00")
            saldo_acreedor = -saldo

        total_debe += td
        total_haber += th
        total_saldo_deudor += saldo_deudor
        total_saldo_acreedor += saldo_acreedor

        lineas.append(
            LineaBalanceComprobacion(
                cuenta_id=row.cuenta_id,
                codigo=row.codigo,
                nombre=row.nombre,
                tipo=row.tipo,
                total_debe=float(td),
                total_haber=float(th),
                saldo_deudor=float(saldo_deudor),
                saldo_acreedor=float(saldo_acreedor),
            )
        )

    return BalanceComprobacionResponse(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        lineas=lineas,
        total_debe=float(total_debe),
        total_haber=float(total_haber),
        total_saldo_deudor=float(total_saldo_deudor),
        total_saldo_acreedor=float(total_saldo_acreedor),
    )


def obtener_estado_resultados(
    db: Session,
    empresa_id: int,
    fecha_desde: date,
    fecha_hasta: date,
) -> EstadoResultadosResponse:

    query = (
        db.query(
            CatalogoCuenta.cuenta_id,
            CatalogoCuenta.codigo,
            CatalogoCuenta.nombre,
            CatalogoCuenta.tipo,
            func.coalesce(func.sum(MovimientoContable.debe), 0).label("total_debe"),
            func.coalesce(func.sum(MovimientoContable.haber), 0).label("total_haber"),
        )
        .join(MovimientoContable, MovimientoContable.cuenta_id == CatalogoCuenta.cuenta_id)
        .filter(
            CatalogoCuenta.empresa_id == empresa_id,
            MovimientoContable.empresa_id == empresa_id,
            MovimientoContable.fecha >= fecha_desde,
            MovimientoContable.fecha <= fecha_hasta,
            CatalogoCuenta.tipo.in_(["INGRESO", "GASTO"]),
        )
        .group_by(
            CatalogoCuenta.cuenta_id,
            CatalogoCuenta.codigo,
            CatalogoCuenta.nombre,
            CatalogoCuenta.tipo,
        )
        .order_by(CatalogoCuenta.codigo)
    )

    ingresos: List[LineaEstadoResultados] = []
    gastos: List[LineaEstadoResultados] = []

    total_ingresos = Decimal("0.00")
    total_gastos = Decimal("0.00")

    for row in query.all():
        td = _dec(row.total_debe)
        th = _dec(row.total_haber)

        if row.tipo == "INGRESO":
            monto = th - td
            total_ingresos += monto
        else:
            monto = td - th
            total_gastos += monto

        linea = LineaEstadoResultados(
            cuenta_id=row.cuenta_id,
            codigo=row.codigo,
            nombre=row.nombre,
            tipo=row.tipo,
            monto=float(monto),
        )

        if row.tipo == "INGRESO":
            ingresos.append(linea)
        else:
            gastos.append(linea)

    utilidad_neta = total_ingresos - total_gastos

    return EstadoResultadosResponse(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        ingresos=ingresos,
        gastos=gastos,
        total_ingresos=float(total_ingresos),
        total_gastos=float(total_gastos),
        utilidad_neta=float(utilidad_neta),
    )


def obtener_balance_general(
    db: Session,
    empresa_id: int,
    fecha_desde: date,
    fecha_hasta: date,
) -> BalanceGeneralResponse:

    query = (
        db.query(
            CatalogoCuenta.cuenta_id,
            CatalogoCuenta.codigo,
            CatalogoCuenta.nombre,
            CatalogoCuenta.tipo,
            func.coalesce(func.sum(MovimientoContable.debe), 0).label("total_debe"),
            func.coalesce(func.sum(MovimientoContable.haber), 0).label("total_haber"),
        )
        .join(MovimientoContable, MovimientoContable.cuenta_id == CatalogoCuenta.cuenta_id)
        .filter(
            CatalogoCuenta.empresa_id == empresa_id,
            MovimientoContable.empresa_id == empresa_id,
            MovimientoContable.fecha >= fecha_desde,
            MovimientoContable.fecha <= fecha_hasta,
            CatalogoCuenta.tipo.in_(["ACTIVO", "PASIVO", "PATRIMONIO"]),
        )
        .group_by(
            CatalogoCuenta.cuenta_id,
            CatalogoCuenta.codigo,
            CatalogoCuenta.nombre,
            CatalogoCuenta.tipo,
        )
        .order_by(CatalogoCuenta.codigo)
    )

    activos: List[LineaBalanceGeneral] = []
    pasivos: List[LineaBalanceGeneral] = []
    patrimonio: List[LineaBalanceGeneral] = []

    total_activos = Decimal("0.00")
    total_pasivos = Decimal("0.00")
    total_patrimonio = Decimal("0.00")

    for row in query.all():
        td = _dec(row.total_debe)
        th = _dec(row.total_haber)

        if row.tipo == "ACTIVO":
            monto = td - th
            total_activos += monto
            activos.append(
                LineaBalanceGeneral(
                    cuenta_id=row.cuenta_id,
                    codigo=row.codigo,
                    nombre=row.nombre,
                    tipo=row.tipo,
                    monto=float(monto),
                )
            )
        else:
            monto = th - td
            if row.tipo == "PASIVO":
                total_pasivos += monto
                pasivos.append(
                    LineaBalanceGeneral(
                        cuenta_id=row.cuenta_id,
                        codigo=row.codigo,
                        nombre=row.nombre,
                        tipo=row.tipo,
                        monto=float(monto),
                    )
                )
            else:
                total_patrimonio += monto
                patrimonio.append(
                    LineaBalanceGeneral(
                        cuenta_id=row.cuenta_id,
                        codigo=row.codigo,
                        nombre=row.nombre,
                        tipo=row.tipo,
                        monto=float(monto),
                    )
                )

    diferencia = total_activos - (total_pasivos + total_patrimonio)

    return BalanceGeneralResponse(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        activos=activos,
        pasivos=pasivos,
        patrimonio=patrimonio,
        total_activos=float(total_activos),
        total_pasivos=float(total_pasivos),
        total_patrimonio=float(total_patrimonio),
        diferencia_activo_pasivo_patrimonio=float(diferencia),
    )
