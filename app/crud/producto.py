from datetime import datetime
from sqlalchemy.orm import Session
from app.models.producto import Producto
from app.schemas.producto import ProductoCrear, ProductoActualizar


def crear_producto(db: Session, datos: ProductoCrear, empresa_id: int, usuario_id: int):
    nuevo = Producto(
        empresa_id=empresa_id,
        codigo=datos.codigo,
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        unidad_medida=datos.unidad_medida,
        cabys=datos.cabys,
        es_inventariable=datos.es_inventariable,
        activo=datos.activo,
        cuenta_inventario_id=datos.cuenta_inventario_id,
        cuenta_costo_venta_id=datos.cuenta_costo_venta_id,
        cuenta_ingreso_id=datos.cuenta_ingreso_id,
        created_by=usuario_id,
        created_at=datetime.utcnow(),
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_productos(db: Session, empresa_id: int, solo_activos: bool = True):
    consulta = db.query(Producto).filter(Producto.empresa_id == empresa_id)
    if solo_activos:
        consulta = consulta.filter(Producto.activo == True)
    return consulta.order_by(Producto.nombre).all()


def obtener_producto(db: Session, empresa_id: int, producto_id: int):
    return (
        db.query(Producto)
        .filter(
            Producto.empresa_id == empresa_id,
            Producto.producto_id == producto_id,
        )
        .first()
    )


def actualizar_producto(db: Session, empresa_id: int, producto_id: int, datos: ProductoActualizar, usuario_id: int):
    producto = obtener_producto(db, empresa_id, producto_id)
    if not producto:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(producto, campo, valor)

    producto.updated_by = usuario_id
    producto.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(producto)
    return producto
