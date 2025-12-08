from datetime import datetime
from sqlalchemy.orm import Session

from app.models.producto_impuesto import ProductoImpuesto
from app.schemas.producto_impuesto import ProductoImpuestoCrear, ProductoImpuestoActualizar


def asignar_impuesto_a_producto(db: Session, datos: ProductoImpuestoCrear):
    existente = (
        db.query(ProductoImpuesto)
        .filter(
            ProductoImpuesto.producto_id == datos.producto_id,
            ProductoImpuesto.impuesto_id == datos.impuesto_id,
        )
        .first()
    )
    if existente:
        existente.tarifa_especifica = datos.tarifa_especifica
        existente.activo = datos.activo
        existente.actualizado_en = datetime.utcnow()
        db.commit()
        db.refresh(existente)
        return existente

    nuevo = ProductoImpuesto(
        producto_id=datos.producto_id,
        impuesto_id=datos.impuesto_id,
        tarifa_especifica=datos.tarifa_especifica,
        activo=datos.activo,
        creado_en=datetime.utcnow(),
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_impuestos_de_producto(db: Session, producto_id: int):
    return (
        db.query(ProductoImpuesto)
        .filter(
            ProductoImpuesto.producto_id == producto_id,
            ProductoImpuesto.activo == True,
        )
        .all()
    )


def actualizar_producto_impuesto(db: Session, producto_impuesto_id: int, datos: ProductoImpuestoActualizar):
    pi = (
        db.query(ProductoImpuesto)
        .filter(ProductoImpuesto.producto_impuesto_id == producto_impuesto_id)
        .first()
    )
    if not pi:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(pi, campo, valor)

    pi.actualizado_en = datetime.utcnow()
    db.commit()
    db.refresh(pi)
    return pi
