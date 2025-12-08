from datetime import datetime
from sqlalchemy.orm import Session

from app.models.impuesto import Impuesto
from app.schemas.impuesto import ImpuestoCrear, ImpuestoActualizar


def crear_impuesto(db: Session, empresa_id: int | None, datos: ImpuestoCrear):
    if datos.es_por_defecto_iva:
        q = db.query(Impuesto).filter(Impuesto.tipo == "IVA", Impuesto.es_por_defecto_iva == True)
        if empresa_id is not None:
            q = q.filter(Impuesto.empresa_id == empresa_id)
        else:
            q = q.filter(Impuesto.empresa_id == None)
        for imp in q.all():
            imp.es_por_defecto_iva = False

    nuevo = Impuesto(
        empresa_id=empresa_id,
        nombre=datos.nombre,
        tipo=datos.tipo,
        codigo_hacienda=datos.codigo_hacienda,
        tarifa=datos.tarifa,
        es_por_defecto_iva=datos.es_por_defecto_iva,
        es_retencion=datos.es_retencion,
        cuenta_contable_id=datos.cuenta_contable_id,
        activo=datos.activo,
        creado_en=datetime.utcnow(),
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_impuestos(db: Session, empresa_id: int | None = None, solo_activos: bool = True):
    q = db.query(Impuesto)
    if empresa_id is None:
        q = q.filter(Impuesto.empresa_id == None)
    else:
        q = q.filter((Impuesto.empresa_id == empresa_id) | (Impuesto.empresa_id == None))

    if solo_activos:
        q = q.filter(Impuesto.activo == True)

    return q.order_by(Impuesto.tipo, Impuesto.nombre).all()


def obtener_impuesto(db: Session, empresa_id: int | None, impuesto_id: int):
    q = db.query(Impuesto).filter(Impuesto.impuesto_id == impuesto_id)
    if empresa_id is None:
        q = q.filter(Impuesto.empresa_id == None)
    else:
        q = q.filter((Impuesto.empresa_id == empresa_id) | (Impuesto.empresa_id == None))
    return q.first()


def actualizar_impuesto(db: Session, empresa_id: int | None, impuesto_id: int, datos: ImpuestoActualizar):
    imp = obtener_impuesto(db, empresa_id, impuesto_id)
    if not imp:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    if cambios.get("es_por_defecto_iva") is True:
        q = db.query(Impuesto).filter(Impuesto.tipo == "IVA", Impuesto.es_por_defecto_iva == True)
        if imp.empresa_id is not None:
            q = q.filter(Impuesto.empresa_id == imp.empresa_id)
        else:
            q = q.filter(Impuesto.empresa_id == None)
        for otro in q.all():
            if otro.impuesto_id != imp.impuesto_id:
                otro.es_por_defecto_iva = False

    for campo, valor in cambios.items():
        setattr(imp, campo, valor)

    imp.actualizado_en = datetime.utcnow()
    db.commit()
    db.refresh(imp)
    return imp
