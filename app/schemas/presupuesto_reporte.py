from pydantic import BaseModel
from typing import Optional, List


class LineaComparativoPresupuesto(BaseModel):
    cuenta_id: int
    codigo_cuenta: str
    nombre_cuenta: str
    centro_costo_id: Optional[int] = None
    mes: Optional[int] = None

    monto_presupuestado: float
    monto_ejecutado: float
    variacion_absoluta: float
    variacion_porcentual: Optional[float]


class ComparativoPresupuestoResponse(BaseModel):
    presupuesto_id: int
    anio: int
    nombre_presupuesto: str
    lineas: List[LineaComparativoPresupuesto]
