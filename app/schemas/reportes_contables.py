from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class LineaBalanceComprobacion(BaseModel):
    cuenta_id: int
    codigo: str
    nombre: str
    tipo: str
    total_debe: float
    total_haber: float
    saldo_deudor: float
    saldo_acreedor: float


class BalanceComprobacionResponse(BaseModel):
    fecha_desde: date
    fecha_hasta: date
    lineas: List[LineaBalanceComprobacion]
    total_debe: float
    total_haber: float
    total_saldo_deudor: float
    total_saldo_acreedor: float


class LineaEstadoResultados(BaseModel):
    cuenta_id: int
    codigo: str
    nombre: str
    tipo: str       # INGRESO o GASTO
    monto: float    # signo normalizado (ingresos positivos, gastos negativos)


class EstadoResultadosResponse(BaseModel):
    fecha_desde: date
    fecha_hasta: date
    ingresos: List[LineaEstadoResultados]
    gastos: List[LineaEstadoResultados]
    total_ingresos: float
    total_gastos: float
    utilidad_neta: float


class LineaBalanceGeneral(BaseModel):
    cuenta_id: int
    codigo: str
    nombre: str
    tipo: str       # ACTIVO, PASIVO, PATRIMONIO
    monto: float


class BalanceGeneralResponse(BaseModel):
    fecha_desde: date
    fecha_hasta: date
    activos: List[LineaBalanceGeneral]
    pasivos: List[LineaBalanceGeneral]
    patrimonio: List[LineaBalanceGeneral]
    total_activos: float
    total_pasivos: float
    total_patrimonio: float
    diferencia_activo_pasivo_patrimonio: float
