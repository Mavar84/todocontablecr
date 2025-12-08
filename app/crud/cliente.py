from datetime import datetime
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCrear, ClienteActualizar


def crear_cliente(db: Session, empresa_id: int, usuario_id: int, datos: ClienteCrear):
    cli = Cliente(
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
    db.add(cli)
    db.commit()
    db.refresh(cli)
    return cli


def listar_clientes(db: Session, empresa_id: int, solo_activos: bool = True):
    q = db.query(Cliente).filter(Cliente.empresa_id == empresa_id)
    if solo_activos:
        q = q.filter(Cliente.activo == True)
    return q.order_by(Cliente.nombre).all()


def obtener_cliente(db: Session, empresa_id: int, cliente_id: int):
    return (
        db.query(Cliente)
        .filter(
            Cliente.empresa_id == empresa_id,
            Cliente.cliente_id == cliente_id,
        )
        .first()
    )


def actualizar_cliente(db: Session, empresa_id: int, cliente_id: int, usuario_id: int, datos: ClienteActualizar):
    cli = obtener_cliente(db, empresa_id, cliente_id)
    if not cli:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(cli, campo, valor)

    cli.actualizado_por = usuario_id
    cli.actualizado_en = datetime.utcnow()

    db.commit()
    db.refresh(cli)
    return cli
