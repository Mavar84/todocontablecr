from datetime import datetime
from sqlalchemy.orm import Session

from app.models.catalogo_cuenta import CatalogoCuenta
from app.schemas.catalogo_cuenta import (
    CatalogoCuentaCreate,
    CatalogoCuentaUpdate,
)


def crear_cuenta(
    db: Session,
    cuenta_in: CatalogoCuentaCreate,
    empresa_id: int,
    usuario_id: int,
):
    nueva = CatalogoCuenta(
        empresa_id=empresa_id,
        codigo=cuenta_in.codigo,
        nombre=cuenta_in.nombre,
        naturaleza=cuenta_in.naturaleza,
        tipo_saldo=cuenta_in.tipo_saldo,
        nivel=cuenta_in.nivel,
        es_imputable=cuenta_in.es_imputable,
        cuenta_padre_id=cuenta_in.cuenta_padre_id,
        es_depreciable=cuenta_in.es_depreciable,
        es_inventario=cuenta_in.es_inventario,
        es_costo=cuenta_in.es_costo,
        activo=cuenta_in.activo,
        created_by=usuario_id,
        created_at=datetime.utcnow(),
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def listar_cuentas(
    db: Session,
    empresa_id: int,
    solo_activas: bool = True,
):
    query = db.query(CatalogoCuenta).filter(CatalogoCuenta.empresa_id == empresa_id)
    if solo_activas:
        query = query.filter(CatalogoCuenta.activo.is_(True))
    return query.order_by(CatalogoCuenta.codigo).all()


def obtener_cuenta_por_id(
    db: Session,
    empresa_id: int,
    cuenta_id: int,
):
    return (
        db.query(CatalogoCuenta)
        .filter(
            CatalogoCuenta.empresa_id == empresa_id,
            CatalogoCuenta.cuenta_id == cuenta_id,
        )
        .first()
    )


def actualizar_cuenta(
    db: Session,
    empresa_id: int,
    cuenta_id: int,
    datos: CatalogoCuentaUpdate,
    usuario_id: int,
):
    cuenta = obtener_cuenta_por_id(db, empresa_id, cuenta_id)
    if not cuenta:
        return None

    data_dict = datos.model_dump(exclude_unset=True)
    for campo, valor in data_dict.items():
        setattr(cuenta, campo, valor)

    cuenta.updated_by = usuario_id
    cuenta.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(cuenta)
    return cuenta


def desactivar_cuenta(
    db: Session,
    empresa_id: int,
    cuenta_id: int,
    usuario_id: int,
):
    cuenta = obtener_cuenta_por_id(db, empresa_id, cuenta_id)
    if not cuenta:
        return None

    cuenta.activo = False
    cuenta.updated_by = usuario_id
    cuenta.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(cuenta)
    return cuenta
