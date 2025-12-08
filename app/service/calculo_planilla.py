from decimal import Decimal
import json
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.empleado import Empleado
from app.models.planilla_evento import PlanillaEvento
from app.models.param_planilla import ParamPlanilla
from app.models.planilla_detalle import PlanillaDetalle


def aplicar_tabla_renta(monto, tabla_json):
    tabla = json.loads(tabla_json)

    for tramo in tabla:
        desde = Decimal(str(tramo["desde"]))
        hasta = tramo["hasta"]
        if hasta is not None:
            hasta = Decimal(str(hasta))

        porcentaje = Decimal(str(tramo["porcentaje"]))

        if hasta is None or (monto >= desde and monto <= hasta):
            return monto * porcentaje

    return Decimal("0")


def calcular_planilla(db: Session, empresa_id: int, planilla):
    params = (
        db.query(ParamPlanilla)
        .filter(ParamPlanilla.empresa_id == empresa_id)
        .first()
    )
    if not params:
        raise ValueError("Debe configurar parámetros de planilla")

    empleados = (
        db.query(Empleado)
        .filter(Empleado.empresa_id == empresa_id, Empleado.activo == True)
        .all()
    )

    total_salarios = Decimal("0")
    total_obrero = Decimal("0")
    total_patrono = Decimal("0")
    total_renta = Decimal("0")
    total_neto = Decimal("0")

    for emp in empleados:
        eventos = (
            db.query(PlanillaEvento)
            .filter(
                PlanillaEvento.empresa_id == empresa_id,
                PlanillaEvento.empleado_id == emp.empleado_id,
                PlanillaEvento.fecha.between(planilla.fecha_pago.replace(day=1), planilla.fecha_pago),
            )
            .all()
        )

        salario = Decimal(str(emp.salario_base))
        horas_extra = Decimal("0")
        monto_extra = Decimal("0")
        incapacidades = Decimal("0")
        vacaciones = Decimal("0")
        bonos = Decimal("0")

        for ev in eventos:
            if ev.tipo == "horas_extra":
                horas_extra += Decimal(str(ev.cantidad))
                monto_extra += Decimal(str(ev.monto))
            elif ev.tipo == "incapacidad":
                incapacidades += Decimal(str(ev.monto))
            elif ev.tipo == "vacaciones":
                vacaciones += Decimal(str(ev.monto))
            elif ev.tipo == "bono":
                bonos += Decimal(str(ev.monto))

        total_dev = salario + monto_extra + incapacidades + vacaciones + bonos

        # Cálculo CCSS obrero
        obrero = salario * (
            params.obrero_ivm +
            params.obrero_enfermedad +
            params.obrero_banco_popular
        )

        # Cálculo CCSS patrono
        patrono = salario * (
            params.patrono_ivm +
            params.patrono_enfermedad +
            params.patrono_asign_fam +
            params.patrono_imf +
            params.patrono_banco_popular
        )

        # Renta
        renta = aplicar_tabla_renta(total_dev, params.renta_tabla_json)

        neto = total_dev - obrero - renta

        det = PlanillaDetalle(
            planilla_id=planilla.planilla_id,
            empleado_id=emp.empleado_id,
            salario_base=salario,
            horas_extra=horas_extra,
            monto_horas_extra=monto_extra,
            incapacidades=incapacidades,
            vacaciones=vacaciones,
            bonos=bonos,
            total_devengado=total_dev,
            total_obrero=obrero,
            total_patrono=patrono,
            renta=renta,
            neto_pagar=neto,
        )

        db.add(det)

        total_salarios += salario
        total_obrero += obrero
        total_patrono += patrono
        total_renta += renta
        total_neto += neto

    planilla.total_salarios = total_salarios
    planilla.total_obrero = total_obrero
    planilla.total_patrono = total_patrono
    planilla.total_renta = total_renta
    planilla.total_neto = total_neto

    planilla.actualizado_en = datetime.utcnow()

    db.commit()

    return planilla
