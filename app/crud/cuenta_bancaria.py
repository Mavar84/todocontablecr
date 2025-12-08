from datetime import datetime
from sqlalchemy.orm import Session
from app.models.cuenta_bancaria import CuentaBancaria
from app.schemas.cuenta_bancaria import CuentaBancariaCrear, CuentaBancariaActualizar


def crear_cuenta_bancaria(db: Session, datos: CuentaBancariaCrear, empresa_id: int, usuario_id: int):
    nueva = CuentaBancaria(
        empresa_id=empresa_id,
        banco_nombre=datos.banco_nombre,
        numero_cuenta=datos.numero_cuenta,
        descripcion=datos.descripcion,
        moneda_id=datos.moneda_id,
        saldo_inicial=datos.saldo_inicial,
        activa=datos.activa,
        created_by=usuario_id,
        created_at=datetime.utcnow(),
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def listar_cuentas_bancarias(db: Session, empresa_id: int, solo_activas: bool = True):
    consulta = db.query(CuentaBancaria).filter(CuentaBancaria.empresa_id == empresa_id)
    if solo_activas:
        consulta = consulta.filter(CuentaBancaria.activa == True)
    return consulta.order_by(CuentaBancaria.banco_nombre, CuentaBancaria.numero_cuenta).all()


def obtener_cuenta_bancaria(db: Session, empresa_id: int, cuenta_bancaria_id: int):
    return (
        db.query(CuentaBancaria)
        .filter(
            CuentaBancaria.empresa_id == empresa_id,
            CuentaBancaria.cuenta_bancaria_id == cuenta_bancaria_id,
        )
        .first()
    )


def actualizar_cuenta_bancaria(db: Session, empresa_id: int, cuenta_bancaria_id: int, datos: CuentaBancariaActualizar, usuario_id: int):
    cuenta = obtener_cuenta_bancaria(db, empresa_id, cuenta_bancaria_id)
    if not cuenta:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(cuenta, campo, valor)

    cuenta.updated_by = usuario_id
    cuenta.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(cuenta)
    return cuenta
