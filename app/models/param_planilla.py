from sqlalchemy import Column, Integer, Numeric, String, ForeignKey
from database import Base


class ParamPlanilla(Base):
    __tablename__ = "param_planilla"

    param_id = Column(Integer, primary_key=True)
    empresa_id = Column(Integer, ForeignKey("empresa.empresa_id"), nullable=False)

    # CCSS – trabajador
    obrero_ivm = Column(Numeric(5, 4), nullable=False)       # % IVM
    obrero_enfermedad = Column(Numeric(5, 4), nullable=False)
    obrero_banco_popular = Column(Numeric(5, 4), nullable=False)

    # CCSS – patrono
    patrono_ivm = Column(Numeric(5, 4), nullable=False)
    patrono_enfermedad = Column(Numeric(5, 4), nullable=False)
    patrono_asign_fam = Column(Numeric(5, 4), nullable=False)
    patrono_imf = Column(Numeric(5, 4), nullable=False)
    patrono_banco_popular = Column(Numeric(5, 4), nullable=False)

    # INS riesgos
    ins_rt = Column(Numeric(5, 4), nullable=False)

    # Renta
    renta_tabla_json = Column(String, nullable=False)  # JSON con los tramos
