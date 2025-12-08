from datetime import datetime
from sqlalchemy.orm import Session

from app.models.proveedor import Proveedor
from app.schemas.proveedor import ProveedorCrear, ProveedorActualizar


def crear_proveedor(db: Session, empresa_id: int, usuario_id: int, datos: ProveedorCrear):
    prv = Proveedor(
        empresa_id=empresa_id,
        nombre=datos.nombre,
        identificacion=datos.identificacion,
        tipo_identificacion=datos.tipo_identificacion,
        correo=datos.correo,
        telefono=datos.telefono,
        direccion=datos.direccion,
        limite_credito=datos.limite_credito,
        dias_credito=datos.dias_credito,
        activo=datos.activo,
        creado_por=usuario_id,
        creado_en=datetime.utcnow(),
    )
    db.add(prv)
    db.commit()
    db.refresh(prv)
    return prv


def listar_proveedores(db: Session, empresa_id: int, solo_activos: bool = True):
    q = db.query(Proveedor).filter(Proveedor.empresa_id == empresa_id)
    if solo_activos:
        q = q.filter(Proveedor.activo == True)
    return q.order_by(Proveedor.nombre).all()


def obtener_proveedor(db: Session, empresa_id: int, proveedor_id: int):
    return (
        db.query(Proveedor)
        .filter(
            Proveedor.empresa_id == empresa_id,
            Proveedor.proveedor_id == proveedor_id,
        )
        .first()
    )


def actualizar_proveedor(db: Session, empresa_id: int, proveedor_id: int, usuario_id: int, datos: ProveedorActualizar):
    prv = obtener_proveedor(db, empresa_id, proveedor_id)
    if not prv:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(prv, campo, valor)

    prv.actualizado_por = usuario_id
    prv.actualizado_en = datetime.utcnow()

    db.commit()
    db.refresh(prv)
    return prv
