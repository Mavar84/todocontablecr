from pydantic import BaseModel
from typing import Optional


class ParamPlanillaBase(BaseModel):
    obrero_ivm: float
    obrero_enfermedad: float
    obrero_banco_popular: float

    patrono_ivm: float
    patrono_enfermedad: float
    patrono_asign_fam: float
    patrono_imf: float
    patrono_banco_popular: float

    ins_rt: float

    renta_tabla_json: str


class ParamPlanillaCrear(ParamPlanillaBase):
    pass


class ParamPlanillaOut(ParamPlanillaBase):
    param_id: int
    empresa_id: int

    class Config:
        from_attributes = True
