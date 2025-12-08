from sqlalchemy.orm import Session
from datetime import date
from app.crud.comprobante import crear_comprobante_automatico
from app.models.planilla_detalle import PlanillaDetalle
from app.models.planilla import Planilla


def contabilizar_planilla(db: Session, empresa_id: int, usuario_id: int, planilla_id: int, cuentas):
    """
    cuentas = dict(
        sueldos_por_pagar= x,
        gastos_personal= x,
        obrero_por_pagar= x,
        patrono_por_pagar= x,
        renta_por_pagar= x,
    )
    """
    planilla = db.query(Planilla).filter(
        Planilla.empresa_id == empresa_id,
        Planilla.planilla_id == planilla_id
    ).first()

    if not planilla:
        raise ValueError("Planilla no encontrada")

    detalles = db.query(PlanillaDetalle).filter(
        PlanillaDetalle.planilla_id == planilla_id
    ).all()

    total_salarios = sum([d.total_devengado for d in detalles])
    total_obrero = sum([d.total_obrero for d in detalles])
    total_patrono = sum([d.total_patrono for d in detalles])
    total_renta = sum([d.renta for d in detalles])
    total_neto = sum([d.neto_pagar for d in detalles])

    lineas = []

    lineas.append({"cuenta_id": cuentas["gastos_personal"], "debe": float(total_salarios), "haber": 0,
                   "detalle": "Gastos de personal"})

    lineas.append({"cuenta_id": cuentas["obrero_por_pagar"], "debe": 0, "haber": float(total_obrero),
                   "detalle": "Deducciones obrero CCSS"})

    lineas.append({"cuenta_id": cuentas["patrono_por_pagar"], "debe": 0, "haber": float(total_patrono),
                   "detalle": "Aporte patronal CCSS"})

    lineas.append({"cuenta_id": cuentas["renta_por_pagar"], "debe": 0, "haber": float(total_renta),
                   "detalle": "Renta por pagar"})

    lineas.append({"cuenta_id": cuentas["sueldos_por_pagar"], "debe": 0, "haber": float(total_neto),
                   "detalle": "Sueldos netos por pagar"})

    comprob = crear_comprobante_automatico(
        db=db,
        empresa_id=empresa_id,
        usuario_id=usuario_id,
        fecha=date.today(),
        descripcion=f"Contabilización de planilla {planilla.periodo}",
        lineas=lineas,
        tipo="PLANILLA",
        referencia_id=planilla_id
    )

    planilla.estado = "contabilizada"
    db.commit()
    return comprob
