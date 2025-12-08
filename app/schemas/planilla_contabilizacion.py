from pydantic import BaseModel


class PlanillaContabilizacionCuentas(BaseModel):
    gastos_personal: int
    sueldos_por_pagar: int
    obrero_por_pagar: int
    patrono_por_pagar: int
    renta_por_pagar: int
