from pydantic import BaseModel


class ConfigContableProduccionBase(BaseModel):
    cuenta_pip_id: int
    cuenta_mp_id: int
    cuenta_mo_id: int
    cuenta_cif_id: int
    cuenta_pt_id: int


class ConfigContableProduccionCrear(ConfigContableProduccionBase):
    pass


class ConfigContableProduccion(ConfigContableProduccionBase):
    config_id: int
    empresa_id: int

    class Config:
        from_attributes = True
