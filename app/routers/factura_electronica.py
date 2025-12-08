from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.core.auth import get_current_user
from app.schemas.factura_electronica import (
    FacturaElectronicaCrear,
    FacturaElectronicaActualizar,
    FacturaElectronica,
)
from app.crud.factura_electronica import (
    crear_factura_electronica,
    obtener_fe,
    obtener_fe_por_factura,
    actualizar_estado_fe,
)

router = APIRouter(prefix="/factura-electronica", tags=["Factura electrónica - emisión"])


@router.post("/", response_model=FacturaElectronica)
def registrar_documento(
    datos: FacturaElectronicaCrear,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    existente = obtener_fe_por_factura(db, usuario.empresa_id, datos.factura_id)
    if existente:
        raise HTTPException(400, "Ya existe un documento electrónico asociado a esta factura")
    return crear_factura_electronica(db, usuario.empresa_id, usuario.usuario_id, datos)


@router.get("/por-factura/{factura_id}", response_model=FacturaElectronica)
def obtener_por_factura(
    factura_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    fe = obtener_fe_por_factura(db, usuario.empresa_id, factura_id)
    if not fe:
        raise HTTPException(404, "Documento electrónico no encontrado para esta factura")
    return fe


@router.get("/{fe_id}", response_model=FacturaElectronica)
def obtener_por_id(
    fe_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    fe = obtener_fe(db, usuario.empresa_id, fe_id)
    if not fe:
        raise HTTPException(404, "Documento electrónico no encontrado")
    return fe


@router.put("/{fe_id}", response_model=FacturaElectronica)
def actualizar_estado(
    fe_id: int,
    datos: FacturaElectronicaActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    fe = actualizar_estado_fe(db, usuario.empresa_id, fe_id, usuario.usuario_id, datos)
    if not fe:
        raise HTTPException(404, "Documento electrónico no encontrado")
    return fe
