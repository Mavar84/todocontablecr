from datetime import datetime
from sqlalchemy.orm import Session

from app.models.configuracion_fe import ConfiguracionFE
from app.schemas.configuracion_fe import ConfiguracionFECrear, ConfiguracionFEActualizar


def obtener_configuracion_fe(db: Session, empresa_id: int):
    return (
        db.query(ConfiguracionFE)
        .filter(ConfiguracionFE.empresa_id == empresa_id)
        .first()
    )


def crear_o_actualizar_configuracion_fe(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    datos: ConfiguracionFECrear | ConfiguracionFEActualizar,
):
    config = obtener_configuracion_fe(db, empresa_id)

    if config is None:
        config = ConfiguracionFE(
            empresa_id=empresa_id,
            tipo_ambiente=datos.tipo_ambiente,
            cedula_emisor=datos.cedula_emisor if hasattr(datos, "cedula_emisor") else "",
            nombre_comercial=getattr(datos, "nombre_comercial", None),
            correo_notificacion=getattr(datos, "correo_notificacion", None),
            sucursal=getattr(datos, "sucursal", None),
            terminal=getattr(datos, "terminal", None),
            codigo_pais_telefono=getattr(datos, "codigo_pais_telefono", None),
            telefono=getattr(datos, "telefono", None),
            usuario_api=getattr(datos, "usuario_api", None),
            clave_api=getattr(datos, "clave_api", None),
            certificado_activo_id=getattr(datos, "certificado_activo_id", None),
            activo=getattr(datos, "activo", True),
            creado_por=usuario_id,
            creado_en=datetime.utcnow(),
        )
        db.add(config)
    else:
        cambios = datos.model_dump(exclude_unset=True)
        for campo, valor in cambios.items():
            setattr(config, campo, valor)
        config.actualizado_por = usuario_id
        config.actualizado_en = datetime.utcnow()

    db.commit()
    db.refresh(config)
    return config
