from pydantic import BaseModel
from typing import List


class CajaChicaRendicionAsignacion(BaseModel):
    rendicion_id: int
    gastos_ids: List[int]
