from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.inventario_saldo import InventarioSaldo
from app.models.inventario_movimiento import InventarioMovimiento
from app.schemas.inventario import MovimientoInventarioCrear


def _dec(valor: float | None) -> Decimal:
    if valor is None:
        return Decimal("0.0000")
    return Decimal(str(valor))


def obtener_saldo(
    db: Session,
    empresa_id: int,
    producto_id: int,
    bodega_id: int,
) -> InventarioSaldo | None:
    return (
        db.query(InventarioSaldo)
        .filter(
            InventarioSaldo.empresa_id == empresa_id,
            InventarioSaldo.producto_id == producto_id,
            InventarioSaldo.bodega_id == bodega_id,
        )
        .first()
    )


def obtener_o_crear_saldo(
    db: Session,
    empresa_id: int,
    producto_id: int,
    bodega_id: int,
) -> InventarioSaldo:
    saldo = obtener_saldo(db, empresa_id, producto_id, bodega_id)
    if saldo:
        return saldo

    nuevo = InventarioSaldo(
        empresa_id=empresa_id,
        producto_id=producto_id,
        bodega_id=bodega_id,
        cantidad=Decimal("0.0000"),
        costo_promedio=Decimal("0.0000"),
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def registrar_movimiento(
    db: Session,
    datos: MovimientoInventarioCrear,
    empresa_id: int,
    usuario_id: int,
):
    cantidad = _dec(datos.cantidad)
    costo_unitario = _dec(datos.costo_unitario)

    if datos.tipo not in ("entrada", "salida"):
        raise ValueError("Tipo de movimiento inválido. Debe ser 'entrada' o 'salida'.")

    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a cero.")

    saldo = obtener_o_crear_saldo(db, empresa_id, datos.producto_id, datos.bodega_id)

    if datos.tipo == "salida" and saldo.cantidad < cantidad:
        raise ValueError("No hay existencia suficiente para realizar la salida.")

    if datos.tipo == "entrada":
        costo_total_nuevo = cantidad * costo_unitario
        costo_total_existente = saldo.cantidad * saldo.costo_promedio
        nueva_cantidad = saldo.cantidad + cantidad

        if nueva_cantidad > 0:
            nuevo_costo_promedio = (costo_total_existente + costo_total_nuevo) / nueva_cantidad
        else:
            nuevo_costo_promedio = Decimal("0.0000")

        saldo.cantidad = nueva_cantidad
        saldo.costo_promedio = nuevo_costo_promedio

    elif datos.tipo == "salida":
        saldo.cantidad = saldo.cantidad - cantidad

    movimiento = InventarioMovimiento(
        empresa_id=empresa_id,
        producto_id=datos.producto_id,
        bodega_id=datos.bodega_id,
        fecha=datos.fecha,
        tipo=datos.tipo,
        referencia=datos.referencia,
        origen=datos.origen,
        origen_id=datos.origen_id,
        cantidad=cantidad,
        costo_unitario=costo_unitario if datos.tipo == "entrada" else saldo.costo_promedio,
        costo_total=cantidad * (costo_unitario if datos.tipo == "entrada" else saldo.costo_promedio),
        comprobante_id=datos.comprobante_id,
        created_by=usuario_id,
        created_at=datetime.utcnow(),
    )

    db.add(movimiento)
    db.commit()
    db.refresh(saldo)
    db.refresh(movimiento)
    return movimiento


def listar_movimientos(
    db: Session,
    empresa_id: int,
    producto_id: int | None = None,
    bodega_id: int | None = None,
):
    consulta = db.query(InventarioMovimiento).filter(InventarioMovimiento.empresa_id == empresa_id)

    if producto_id is not None:
        consulta = consulta.filter(InventarioMovimiento.producto_id == producto_id)
    if bodega_id is not None:
        consulta = consulta.filter(InventarioMovimiento.bodega_id == bodega_id)

    return consulta.order_by(
        InventarioMovimiento.fecha.desc(),
        InventarioMovimiento.movimiento_inventario_id.desc()
    ).all()
